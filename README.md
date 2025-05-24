# LNK_Structure_Reader

This is a simple tool written in **Python** for inspecting and parsing the structure of `.lnk` files (Windows shortcuts).

## Supported Structures

Currently, this tool can parse the following parts of a `.lnk` file:
- Header
- LinkTargetIDList
- LinkInfo
- StringData
- ExtraData

## How to Use

You can run it with the following command:
```bash
python lnk_parser.py path/to/your/file.lnk
```
It will print the structure and information of the `.lnk` file to the terminal.

## Contributions Welcome

This is a small project I created for learning and experimentation. The code quality may not be great, and there might be some bugs.
If you find any issues, errors, or better ways to implement things, you're very welcome to:

- Open an issue to discuss
- Fork the project and submit a pull request
- Use this tool as a base for your own experiments or applications

Any help or feedback is highly appreciated!

## Disclaimer

- This tool only parses parts of the `.lnk` file format and does not guarantee completeness or accuracy.
- If you're interested in the .lnk file format, check out the official spec: [Microsoft Shell Link (.LNK) Binary File Format](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943)

## License
This project is licensed under the MIT License.
