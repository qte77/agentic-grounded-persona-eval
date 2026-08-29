from scripts.verify_sourcing import find_unsourced_quotes


def test_sourced_quote_passes():
    markdown = (
        '> "Fragmentation is the whole problem."\n'
        "> — someone, 2024-01-01, [HN #1](https://news.ycombinator.com/item?id=1)\n"
    )
    assert find_unsourced_quotes(markdown) == []


def test_unsourced_quote_flagged():
    markdown = '> "This has no attribution at all."\n> just more text, still no link\n'
    violations = find_unsourced_quotes(markdown)
    assert len(violations) == 1
    assert violations[0].start_line == 1


def test_mixed_blocks_only_flags_the_unsourced_one():
    markdown = (
        '> "Sourced one."\n'
        "> — a, 2024-01-01, [HN #1](https://news.ycombinator.com/item?id=1)\n"
        "\n"
        "Some prose in between, not a quote.\n"
        "\n"
        '> "Unsourced one."\n'
        "> no link here\n"
    )
    violations = find_unsourced_quotes(markdown)
    assert len(violations) == 1
    assert "Unsourced one" in violations[0].snippet


def test_non_quote_content_ignored():
    markdown = "# Heading\n\nJust a normal paragraph with a [link](https://example.com) in it.\n"
    assert find_unsourced_quotes(markdown) == []


def test_multiline_attribution_with_link_passes():
    markdown = (
        '> "Long quote spanning context."\n'
        "> — vitovito, 2014-10-22, [HN #1](https://news.ycombinator.com/item?id=1) (combined with\n"
        ">   dawhizkid, 2018-02-18, [HN #2](https://news.ycombinator.com/item?id=2))\n"
    )
    assert find_unsourced_quotes(markdown) == []


def test_no_findings_file_is_trivially_empty():
    assert find_unsourced_quotes("") == []
