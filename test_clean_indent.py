html_test = """
    <div style="background:#000;">
        <div style="display:flex;">
            <span>Test</span>
        </div>
    </div>
"""

clean = "\n".join([line.strip() for line in html_test.split("\n") if line.strip()])
print("Any 4-space indent?", any(l.startswith("    ") for l in clean.split("\n")))
print("Clean:")
print(clean)
