import chess.engine

class ChessEngine:
    def __init__(self, engine_path, time_limit=1.0):
        self.engine_path = engine_path
        self.engine = None
        self.time_limit = time_limit

    def get_best_move(self, board: chess.Board) -> chess.Move:
        if self.engine is None:
            raise RuntimeError("Engine is not started")
        results = self.engine.play(
            board,
            limit=chess.engine.Limit(time=self.time_limit)
        )
        return results.move

    def __enter__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.engine_path
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.quit()
            self.engine = None