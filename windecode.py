import argparse
import re

# === Lookup Tables ===

edition_map = {
    "UL": "Ultimate", "PR": "Professional", "HO": "Home Premium",
    "EN": "Enterprise", "BS": "Business", "HB": "Home Basic",
    "EDU": "Education", "CORE": "Home", "PRO": "Professional",
}

arch_map = {
    "X": "x86 (32-bit)", "X86": "x86 (32-bit)", "X64": "x64 (64-bit)",
    "AMD64": "x64 (64-bit)", "ARM64": "ARM64",
}

channel_map = {
    "FRE": "Retail", "CHK": "Debug/Checked", "VOL": "Volume License"
}

sp_map = {
    "GSP1": "Service Pack 1", "SP0": "No Service Pack",
    "SP2": "Service Pack 2", "GDR": "General Distribution Release"
}

# === Decoding Logic ===

def decode_filename(name: str) -> dict:
    clean_name = name.upper().replace("-", "_").replace(".", "_")
    parts = clean_name.split("_")

    result = {
        "Raw Filename": name,
        "Detected OS": None,
        "Edition": None,
        "Architecture": None,
        "Service Pack": None,
        "Language": None,
        "Channel": None,
        "Build": None,
        "Notes": [],
    }

    for part in parts:
        # OS Identification
        if part.startswith("GSP"):
            result["Service Pack"] = sp_map.get(part, "Unknown SP")
            result["Detected OS"] = "Windows 7"
        if part.startswith("GRMC"):
            result["Detected OS"] = "Windows Vista or 7"
        if "WIN7" in part:
            result["Detected OS"] = "Windows 7"
        elif "WIN8" in part:
            result["Detected OS"] = "Windows 8"
        elif "WIN10" in part:
            result["Detected OS"] = "Windows 10"
        elif "WIN11" in part:
            result["Detected OS"] = "Windows 11"

        # Edition
        for ed in edition_map:
            if ed in part:
                result["Edition"] = edition_map[ed]

        # Architecture
        for arch in arch_map:
            if arch in part:
                result["Architecture"] = arch_map[arch]

        # Channel
        for ch in channel_map:
            if ch in part:
                result["Channel"] = channel_map[ch]

        # Language
        if re.match(r"EN(-|_)?US", part):
            result["Language"] = "English (US)"
        elif part == "EN":
            result["Language"] = "English"

        # Build Numbers
        if re.match(r"\d{5,6}", part):
            result["Build"] = part

    # Fallback guessing
    if not result["Detected OS"] and "WINDOWS" in clean_name:
        if "7" in clean_name:
            result["Detected OS"] = "Windows 7"
        elif "8" in clean_name:
            result["Detected OS"] = "Windows 8"
        elif "10" in clean_name:
            result["Detected OS"] = "Windows 10"
        elif "11" in clean_name:
            result["Detected OS"] = "Windows 11"

    return result

# === Output Formatter ===

def print_result(decoded: dict):
    for key, value in decoded.items():
        print(f"{key}: {value if value else 'Unknown'}")

# === Main CLI Entry ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode any Windows ISO filename into a human-readable format")
    parser.add_argument("filename", help="The ISO filename to decode")
    args = parser.parse_args()

    result = decode_filename(args.filename)
    print_result(result)
