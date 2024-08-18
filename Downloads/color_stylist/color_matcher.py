def match_colors(tops, bottoms):
    color_combinations = {
        "White": ["Black", "Navy", "Red", "Blue", "Green"],
        "Black": ["White", "Red", "Grey", "Yellow"],
        "Red": ["White", "Black", "Grey", "Blue"],
        "Blue": ["White", "Grey", "Brown", "Green"],
        "Green": ["White", "Brown", "Grey", "Black"],
        "Yellow": ["Black", "Grey", "Navy"],
    }
    matches = []
    for top in tops:
        for bottom in bottoms:
            if bottom in color_combinations.get(top, []) or top in color_combinations.get(bottom, []):
                matches.append((top, bottom))
    return matches