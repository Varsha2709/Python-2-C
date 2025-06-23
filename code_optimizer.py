def loop_optimization_and_basic_blocks(c_code):
    lines = c_code.split('\n')
    optimized = []
    basic_blocks = []
    current_block = []

    # Divide into basic blocks
    for line in lines:
        stripped = line.strip()
        current_block.append(line)
        if stripped.endswith('}') or stripped.startswith('return') or stripped == '}':
            basic_blocks.append(current_block)
            current_block = []

    if current_block:
        basic_blocks.append(current_block)

    # Optimize loop blocks
    optimized_code = []
    for block in basic_blocks:
        block_str = "\n".join(block)
        if "for (" in block_str or "while (" in block_str:
            moved_lines = []
            new_block = []
            for line in block:
                if any(op in line for op in ["*", "/", "pow("]) and "=" in line:
                    moved_lines.append(line)
                else:
                    new_block.append(line)
            if moved_lines:
                optimized_code.extend(["// Loop-invariant code motion:"] + moved_lines)
                optimized_code.extend(new_block)
            else:
                optimized_code.extend(block)
        else:
            optimized_code.extend(block)

    return "\n".join(optimized_code)
