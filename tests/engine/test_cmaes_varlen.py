"""Tests for Variable-Length CMA-ES Strategy."""

import pytest

from strand.engine.strategies.cmaes_varlen import CMAESVarLenStrategy


class TestCMAESVarLenStrategy:
    """Variable-length CMA-ES strategy tests."""

    def test_initialization(self):
        """Test CMAESVarLenStrategy initialization."""
        strategy = CMAESVarLenStrategy(
            alphabet="ACDE",
            min_len=5,
            max_len=20,
            seed=42,
            sigma0=0.3,
        )
        assert strategy.alphabet == "ACDE"
        assert strategy.min_len == 5
        assert strategy.max_len == 20
        assert strategy.sigma0 == 0.3

    def test_ask_returns_variable_length_sequences(self):
        """Test that ask returns sequences with variable lengths."""
        strategy = CMAESVarLenStrategy(
            alphabet="AC",
            min_len=5,
            max_len=15,
            seed=42,
        )
        sequences = strategy.ask(10)
        assert len(sequences) == 10

        # Check all sequences are within bounds
        lengths = [len(seq.tokens) for seq in sequences]
        assert all(5 <= length <= 15 for length in lengths)

        # Check all use valid alphabet
        for seq in sequences:
            assert all(c in "AC" for c in seq.tokens)

        # Should have some variation in lengths
        assert len(set(lengths)) > 1, "Expected variable lengths"

    def test_best_tracking(self):
        """Test that best score is tracked."""
        strategy = CMAESVarLenStrategy(
            alphabet="AC",
            min_len=5,
            max_len=10,
            seed=42,
        )
        assert strategy.best() is None

        sequences = strategy.ask(10)
        items = [(seq, 0.5 + i * 0.05, None) for i, seq in enumerate(sequences)]
        strategy.tell(items)

        best_seq, best_score = strategy.best()
        assert best_seq == sequences[-1]
        assert best_score > 0.9

    def test_invalid_params(self):
        """Test that invalid parameters raise errors."""
        with pytest.raises(ValueError, match="non-empty"):
            CMAESVarLenStrategy(alphabet="", min_len=5, max_len=10)

        with pytest.raises(ValueError, match="invalid"):
            CMAESVarLenStrategy(alphabet="AC", min_len=0, max_len=10)

        with pytest.raises(ValueError, match="invalid"):
            CMAESVarLenStrategy(alphabet="AC", min_len=10, max_len=5)

    def test_state_serialization(self):
        """Test that state is serializable."""
        strategy = CMAESVarLenStrategy(
            alphabet="AC",
            min_len=5,
            max_len=10,
            seed=42,
        )
        sequences = strategy.ask(10)
        items = [(seq, 0.5 + i * 0.05, None) for i, seq in enumerate(sequences)]
        strategy.tell(items)

        state = strategy.state()
        assert "best_score" in state
        assert state["best_score"] > 0.9

    def test_convergence_with_multiple_generations(self):
        """Test that strategy improves over multiple generations."""
        strategy = CMAESVarLenStrategy(
            alphabet="AC",
            min_len=8,
            max_len=12,
            seed=42,
        )

        best_scores = []
        for _gen in range(5):
            sequences = strategy.ask(16)
            # Simple scoring: prefer longer sequences
            items = [(seq, len(seq.tokens) / 12.0, None) for seq in sequences]
            strategy.tell(items)

            best = strategy.best()
            if best:
                best_scores.append(best[1])

        # Should improve or stay same
        assert len(best_scores) == 5
        assert best_scores[-1] >= best_scores[0]

    def test_decode_handles_length_scaling(self):
        """Test that length is properly scaled."""
        strategy = CMAESVarLenStrategy(
            alphabet="AC",
            min_len=10,
            max_len=20,
            seed=42,
        )

        # Test decoding various continuous vectors
        x1 = [-1.0] * (1 + 20)  # All -1: should give min_len
        seq1 = strategy._decode_sequence(x1)
        assert len(seq1.tokens) >= 10

        x2 = [1.0] * (1 + 20)  # All +1: should give max_len
        seq2 = strategy._decode_sequence(x2)
        assert len(seq2.tokens) <= 20

        # Midpoint should be around (min+max)/2
        x_mid = [0.0] * (1 + 20)
        seq_mid = strategy._decode_sequence(x_mid)
        expected_len = (10 + 20) // 2
        assert abs(len(seq_mid.tokens) - expected_len) <= 1

