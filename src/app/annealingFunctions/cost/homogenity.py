from .cost import Cost

class Homogenity(Cost):

    def cost(self, state):
        sin_error = super().cost(state)

        count = 10
        ok = 0
        not_ok = 50
        for x in range(count):
            i = int(random.uniform(1, state.shape[0] - 1))
            j = int(random.uniform(1, state.shape[1] - 1))
            color = state[i][j]
            gotya = 0
            for di in range(3):
                if gotya == 1:
                    break
                for dj in range(3):
                    if di == 1 and dj == 1:
                        continue
                    other_color = state[i - 1 + di][j - 1 + dj]
                    if other_color > color * 0.9 and other_color < color * 1:
                        ok += 1
                        gotya = 1
                        break

        not_ok = count - ok

        return sin_error + 0.01*(not_ok / count)
