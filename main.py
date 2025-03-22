import pyxel

class Game:
    def __init__(self):
        # 画面サイズ 160x120, タイトル "Simple Pong"
        pyxel.init(160, 120, title="Simple Pong")

        # ゲーム開始時の各種パラメータ初期化
        self.reset()

        # メインループ開始
        pyxel.run(self.update, self.draw)

    def reset(self):
        # パドル（バー）の位置
        self.paddle_y = pyxel.height // 2 - 10  # パドルの中心を画面中央に
        # ボールの初期位置
        self.ball_x = pyxel.width // 2
        self.ball_y = pyxel.height // 2
        # ボールの速度
        self.ball_vx = -2
        self.ball_vy = 2
        # スコアとゲームオーバーフラグ
        self.score = 0
        self.game_over = False

    def update(self):
        # ゲームオーバー時はスペースキーでリセット
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
            return

        # ── パドルの操作 ──
        if pyxel.btn(pyxel.KEY_UP):
            self.paddle_y -= 3
        if pyxel.btn(pyxel.KEY_DOWN):
            self.paddle_y += 3
        # 画面外にはみ出さないよう制限
        self.paddle_y = max(0, min(self.paddle_y, pyxel.height - 20))

        # ── ボールの移動 ──
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # 上下の壁でバウンド
        if self.ball_y < 0 or self.ball_y > pyxel.height - 4:
            self.ball_vy *= -1

        # 左壁でバウンド
        if self.ball_x < 0:
            self.ball_x = 0
            self.ball_vx *= -1

        # ── パドルとの当たり判定 ──
        # 右端パドル（x座標: 画面幅-4）付近にボールが来て、
        # ボールのyがパドルの縦範囲内なら跳ね返す
        if (self.ball_x > pyxel.width - 8 and
            self.paddle_y < self.ball_y < self.paddle_y + 20):
            self.ball_x = pyxel.width - 8
            self.ball_vx *= -1
            self.score += 1  # 跳ね返した回数がスコア

        # 画面右端を越えたらゲームオーバー
        if self.ball_x > pyxel.width:
            self.game_over = True

    def draw(self):
        pyxel.cls(0)

        if self.game_over:
            pyxel.text(60, 50, "GAME OVER!", pyxel.COLOR_WHITE)
            pyxel.text(50, 70, f"Score: {self.score}", pyxel.COLOR_WHITE)
            pyxel.text(30, 90, "Press SPACE to restart", pyxel.COLOR_WHITE)
            return

        # ── パドル描画（白色）──
        pyxel.rect(pyxel.width - 4, self.paddle_y, 4, 20, pyxel.COLOR_WHITE)

        # ── ボール描画（白色 4x4）──
        pyxel.rect(self.ball_x, self.ball_y, 4, 4, pyxel.COLOR_WHITE)

        # ── スコア表示 ──
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)

# ゲーム開始
Game()
