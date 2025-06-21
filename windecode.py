# windecode_ultimate.py
# A massive standalone Windows ISO decoder script with support for ALL major versions

import argparse
import re

# === Full Windows Build Map ===
build_map = {
    # Classic Windows (No build numbers in filenames, but included for completeness)
    "00001": {"Name": "Windows 1.0", "Codename": "Interface Manager", "Release": "1985-11-20"},
    "00002": {"Name": "Windows 2.0", "Codename": "Windows/286 & Windows/386", "Release": "1987-12-09"},
    "00300": {"Name": "Windows 3.0", "Codename": "Windows 3", "Release": "1990-05-22"},
    "00310": {"Name": "Windows 3.1", "Codename": "Janus", "Release": "1992-04-06"},
    "00311": {"Name": "Windows for Workgroups 3.11", "Codename": "Snowball", "Release": "1993-11-08"},
    "00400": {"Name": "Windows 95", "Codename": "Chicago", "Release": "1995-08-24"},
    "00410": {"Name": "Windows 98", "Codename": "Memphis", "Release": "1998-06-25"},
    "00490": {"Name": "Windows 98 Second Edition", "Codename": "Memphis SE", "Release": "1999-05-05"},
    "30000": {"Name": "Windows ME", "Codename": "Millennium", "Release": "2000-09-14"},

    # NT-era and modern builds
    "2195": {"Name": "Windows 2000", "Codename": "Windows 2000", "Release": "2000-02-17"},
    "2600": {"Name": "Windows XP RTM/SP1/SP2/SP3", "Codename": "Whistler", "Release": "2001-10-25"},
    "3790": {"Name": "Windows Server 2003 / XP x64", "Codename": "Server 2003", "Release": "2003-04-24"},
    "4033": {"Name": "Windows Longhorn M3", "Codename": "Longhorn", "Release": "2003-06-30"},
    "5048": {"Name": "Windows Vista Beta 1", "Codename": "Longhorn", "Release": "2005-04-01"},
    "5112": {"Name": "Windows Vista Beta 1 Refresh", "Codename": "Longhorn", "Release": "2005-07-27"},
    "5219": {"Name": "Windows Vista Beta 2 Preview", "Codename": "Longhorn", "Release": "2005-09-01"},
    "5308": {"Name": "Windows Vista CTP February", "Codename": "Longhorn", "Release": "2006-02-01"},
    "5384": {"Name": "Windows Vista Beta 2", "Codename": "Longhorn", "Release": "2006-05-23"},
    "5456": {"Name": "Windows Vista Pre-RC1", "Codename": "Longhorn", "Release": "2006-06-28"},
    "5472": {"Name": "Windows Vista Pre-RC1 Refresh", "Codename": "Longhorn", "Release": "2006-07-17"},
    "5536": {"Name": "Windows Vista RC1 Escrow", "Codename": "Longhorn", "Release": "2006-08-17"},
    "5600": {"Name": "Windows Vista RC1", "Codename": "Longhorn", "Release": "2006-08-29"},
    "5744": {"Name": "Windows Vista RC2", "Codename": "Longhorn", "Release": "2006-10-06"},
    "5808": {"Name": "Windows Vista RTM Escrow", "Codename": "Longhorn", "Release": "2006-10-17"},
    "5840": {"Name": "Windows Vista RTM Escrow", "Codename": "Longhorn", "Release": "2006-10-24"},
    "6000": {"Name": "Windows Vista RTM", "Codename": "Vista", "Release": "2007-01-30"},
    "6001": {"Name": "Windows Vista SP1", "Codename": "Vista SP1", "Release": "2008-03-18"},
    "6002": {"Name": "Windows Vista SP2", "Codename": "Vista SP2", "Release": "2009-04-28"},
    "7600": {"Name": "Windows 7 RTM", "Codename": "Windows 7", "Release": "2009-10-22"},
    "7601": {"Name": "Windows 7 SP1", "Codename": "Windows 7 SP1", "Release": "2011-02-22"},
    "9200": {"Name": "Windows 8 RTM / Server 2012", "Codename": "Windows 8", "Release": "2012-10-26"},
    "9600": {"Name": "Windows 8.1 / Server 2012 R2", "Codename": "Blue", "Release": "2013-10-17"},
    "10240": {"Name": "Windows 10 RTM", "Codename": "Threshold 1", "Release": "2015-07-29"},
    "10586": {"Name": "Windows 10 November Update", "Codename": "Threshold 2", "Release": "2015-11-10"},
    "14393": {"Name": "Windows 10 Anniversary Update / Server 2016", "Codename": "Redstone 1", "Release": "2016-08-02"},
    "15063": {"Name": "Windows 10 Creators Update", "Codename": "Redstone 2", "Release": "2017-04-05"},
    "16299": {"Name": "Windows 10 Fall Creators Update", "Codename": "Redstone 3", "Release": "2017-10-17"},
    "17134": {"Name": "Windows 10 April 2018 Update", "Codename": "Redstone 4", "Release": "2018-04-30"},
    "17763": {"Name": "Windows 10 October 2018 / Server 2019", "Codename": "Redstone 5", "Release": "2018-10-02"},
    "18362": {"Name": "Windows 10 May 2019 Update", "Codename": "19H1", "Release": "2019-05-21"},
    "18363": {"Name": "Windows 10 November 2019 Update", "Codename": "19H2", "Release": "2019-11-12"},
    "19041": {"Name": "Windows 10 May 2020 Update", "Codename": "20H1", "Release": "2020-05-27"},
    "19042": {"Name": "Windows 10 October 2020 Update", "Codename": "20H2", "Release": "2020-10-20"},
    "19043": {"Name": "Windows 10 May 2021 Update", "Codename": "21H1", "Release": "2021-05-18"},
    "19044": {"Name": "Windows 10 November 2021 Update", "Codename": "21H2", "Release": "2021-11-16"},
    "19045": {"Name": "Windows 10 22H2", "Codename": "22H2", "Release": "2022-10-18"},
    "20348": {"Name": "Windows Server 2022", "Codename": "Iron", "Release": "2021-08-18"},
    "22000": {"Name": "Windows 11 21H2", "Codename": "Sun Valley 1", "Release": "2021-10-05"},
    "22621": {"Name": "Windows 11 22H2", "Codename": "Sun Valley 2", "Release": "2022-09-20"},
    "22631": {"Name": "Windows 11 23H2", "Codename": "Moment 4+", "Release": "2023-10-31"},
    "26100": {"Name": "Windows 11 24H2 (Preview / AI PC Launch)", "Codename": "Hudson Valley", "Release": "2024-05-21"}
}


# === Common Maps ===
edition_map = {
    "ULT": "Ultimate", "UL": "Ultimate", "PR": "Professional", "PRO": "Professional",
    "HO": "Home Premium", "CORE": "Home", "EN": "Enterprise", "EDU": "Education",
    "HB": "Home Basic", "BS": "Business", "STD": "Standard", "DATACENTER": "Datacenter",
    "SERVER": "Server"
}

arch_map = {
    "X86": "x86 (32-bit)", "X64": "x64 (64-bit)", "AMD64": "x64 (64-bit)",
    "ARM64": "ARM64", "IA64": "Itanium (IA-64)", "X": "x86 (32-bit)"
}

channel_map = {
    "FRE": "Retail", "CHK": "Debug/Checked", "VOL": "Volume License", "OEM": "OEM"
}

# === Decoder ===
def decode_iso_name(name):
    clean = name.upper().replace("-", "_").replace(".", "_")
    parts = clean.split("_")

    result = {
        "Raw Filename": name,
        "OS": None,
        "Codename": None,
        "Build": None,
        "Update Revision": None,
        "Edition": None,
        "Architecture": None,
        "Channel": None,
        "Language": None,
        "Release Date": None,
        "Notes": []
    }

    for part in parts:
        # Extract major build
        match = re.match(r"(\d{5})[\.]?(\d{0,5})?", part)
        if match:
            base = match.group(1)
            if base in build_map:
                b = build_map[base]
                result["Build"] = base
                result["OS"] = b["Name"]
                result["Codename"] = b["Codename"]
                result["Release Date"] = b["Release"]
            if match.group(2):
                result["Update Revision"] = match.group(2)

        for k, v in edition_map.items():
            if k in part:
                result["Edition"] = v

        for k, v in arch_map.items():
            if k in part:
                result["Architecture"] = v

        for k, v in channel_map.items():
            if k in part:
                result["Channel"] = v

        if part.startswith("EN"):
            result["Language"] = "English (US)"

        if "EVAL" in part:
            result["Edition"] = (result["Edition"] or "") + " Evaluation"

        if part in ["RS1", "RS2", "RS3", "RS4", "RS5"]:
            result["Codename"] = f"Redstone Series ({part})"

        if part == "REFRESH" or "SVC_REFRESH" in part:
            result["Notes"].append("Servicing Refresh")

    if not result["OS"] and "WIN" in clean:
        if "7" in clean:
            result["OS"] = "Windows 7"
        elif "8" in clean:
            result["OS"] = "Windows 8"
        elif "10" in clean:
            result["OS"] = "Windows 10"
        elif "11" in clean:
            result["OS"] = "Windows 11"

    return result

# === CLI ===
def main():
    parser = argparse.ArgumentParser(description="Decode ANY Windows ISO filename into a human-readable form")
    parser.add_argument("filename", help="The ISO filename to decode")
    args = parser.parse_args()

    decoded = decode_iso_name(args.filename)
    for key, value in decoded.items():
        if isinstance(value, list):
            value = ", ".join(value) if value else "None"
        print(f"{key}: {value if value else 'Unknown'}")

if __name__ == "__main__":
    main()
