import zlib, struct, random, base64

N = 112                      # tile size; small enough to stay cheap, big enough
random.seed(20260910)        # not to read as an obvious repeat

# A paper tooth rather than TV static: start from white noise, then blur it
# twice with wrap-around so the tile stays seamless, and quantise the result
# so the PNG's alpha channel compresses well.
buf = [[random.random() for _ in range(N)] for _ in range(N)]
for _ in range(2):
    nxt = [[0.0]*N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            s = 0.0
            for dy in (-1, 0, 1):
                row = buf[(y+dy) % N]
                for dx in (-1, 0, 1):
                    s += row[(x+dx) % N]
            nxt[y][x] = s / 9.0
    # push contrast back up after blurring, around the mean
    m = sum(sum(r) for r in nxt) / (N*N)
    buf = [[m + (v - m) * 2.6 for v in row] for row in nxt]

# a second, finer pass keeps some bite in the grain
fine = [[random.random() for _ in range(N)] for _ in range(N)]
mix  = [[buf[y][x]*0.72 + fine[y][x]*0.28 for x in range(N)] for y in range(N)]
m = sum(sum(r) for r in mix) / (N*N)

INK = (74, 62, 46)           # warm, so it reads as paper and not as dirt
px = bytearray()
for y in range(N):
    for x in range(N):
        d = mix[y][x] - m
        a = int(max(0, min(1, abs(d) * 3.0)) * 26)      # 0..26 alpha
        a = (a // 3) * 3                                 # quantise: smaller PNG
        px += bytes((INK[0], INK[1], INK[2], a if d < 0 else a // 3))

raw = bytearray()
for y in range(N):
    raw.append(0)
    raw += px[y*N*4:(y+1)*N*4]

def chunk(t, b):
    return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t+b) & 0xffffffff)

png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', N, N, 8, 6, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
       + chunk(b'IEND', b''))

b64 = base64.b64encode(png).decode('ascii')
open('grain.b64', 'w').write(b64)
print('tile %dx%d  png %.1f KB  base64 %.1f KB' % (N, N, len(png)/1024, len(b64)/1024))
