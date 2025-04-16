import argparse
import pathlib
import plistlib

# Transformation matrix from Display P3 to sRGB
p3_to_srgb = [
    [1.2249, -0.2247, 0.0000],
    [-0.0421, 1.0419, 0.0000],
    [-0.0197, -0.0786, 1.0979],
]


def convert_p3_to_srgb(rgb_p3):
    rgb_srgb = [0, 0, 0]

    # Convert color using matrix multiplication
    for i in range(3):
        for j in range(3):
            rgb_srgb[i] += p3_to_srgb[i][j] * rgb_p3[j]

    # Clamp values to [0,1] range
    rgb_srgb = [max(0.0, min(1.0, val)) for val in rgb_srgb]

    return rgb_srgb


def process_plist(file_path: pathlib.Path):
    with file_path.open("rb") as f:
        plist = plistlib.load(f)

    # Convert colors
    for key, value in plist.items():
        if isinstance(value, dict) and value.get("Color Space") == "P3":
            (
                value["Red Component"],
                value["Green Component"],
                value["Blue Component"],
            ) = convert_p3_to_srgb(
                (
                    value["Red Component"],
                    value["Green Component"],
                    value["Blue Component"],
                )
            )
            value["Color Space"] = "sRGB"  # Change color space identifier

    # Save updated plist
    output_path = file_path.with_suffix(f".rgb{file_path.suffix}")
    with output_path.open("wb") as f:
        plistlib.dump(plist, f)

    print(file_path, "converted to", output_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="Files to convert", type=pathlib.Path)
    args = ap.parse_args()
    for file_path in args.files:
        process_plist(file_path)


if __name__ == "__main__":
    main()
