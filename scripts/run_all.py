from __future__ import annotations

from generate_note_drafts import generate as generate_note_drafts
from generate_growth_pack import generate as generate_growth_pack
from generate_launch_copy import generate as generate_launch_copy
from build_site import build as build_site
from export_social_queue import export as export_social_queue
from validate_content import validate
from utils import load_json, now_iso, root_path, write_json


def main() -> None:
    note_paths = generate_note_drafts()
    site_paths = build_site()
    social_csv, x_json = export_social_queue()
    growth_paths = generate_growth_pack()
    launch_copy = generate_launch_copy()
    problems = validate()
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)

    history = load_json("data", "history.json")
    history["generated_at"] = now_iso()
    history["published_products"] = []
    history["social_posts"] = [
        {"file": str(social_csv.relative_to(root_path()))},
        {"file": str(x_json.relative_to(root_path()))},
    ]
    history["launch_copy"] = {"file": str(launch_copy.relative_to(root_path()))}
    write_json(root_path("data", "history.json"), history)

    print("Generated note drafts:")
    for path in note_paths:
        print(" -", path.relative_to(root_path()))
    print("Generated site files:", len(site_paths))
    print("Generated social queue:")
    print(" -", social_csv.relative_to(root_path()))
    print(" -", x_json.relative_to(root_path()))
    print("Generated growth pack:")
    for path in growth_paths:
        print(" -", path.relative_to(root_path()))
    print("Generated launch copy:")
    print(" -", launch_copy.relative_to(root_path()))


if __name__ == "__main__":
    main()
