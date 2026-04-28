CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "png", "jpg"]
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "en",
        "toolbar": {
            "items": [
                # Document
                "undo",
                "redo",
                "|",
                "findAndReplace",
                "selectAll",
                "|",
                # Export (requires export plugins in build)
                "exportPdf",
                "exportWord",
                "|",
                # Clipboard (many builds already include pasteFromOffice)
                "cut",
                "copy",
                "paste",
                "pasteText",
                "pasteFromOffice",
                "|",
                # Headings & Styles
                "heading",
                "|",
                # Fonts
                "fontSize",
                "fontFamily",
                "fontColor",
                "fontBackgroundColor",
                "highlight",
                "|",
                # Formatting
                "bold",
                "italic",
                "underline",
                "strikethrough",
                "code",
                "subscript",
                "superscript",
                "removeFormat",
                "|",
                # Paragraph / Lists / Indentation
                "alignment",
                "bulletedList",
                "numberedList",
                "todoList",
                "outdent",
                "indent",
                "horizontalLine",
                "specialCharacters",
                "pageBreak",
                "|",
                # Links
                "link",
                "|",
                # Quotes & Code
                "blockQuote",
                "codeBlock",
                "|",
                # Media
                "insertTable",
                "imageUpload",
                "mediaEmbed",
                "htmlEmbed",
                "|",
                # Tools
                "sourceEditing",
            ],
            "shouldNotGroupWhenFull": True,
        },
        # Font configuration
        "fontFamily": {
            "options": [
                "default",
                "Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
                "Georgia, serif",
                "Times New Roman, Times, serif",
                "Trebuchet MS, Helvetica, sans-serif",
                "Tahoma, Verdana, sans-serif",
                "Courier New, Courier, monospace",
                "Fira Code, Menlo, Consolas, 'Liberation Mono', monospace",
            ],
            "supportAllValues": True,  # allow custom CSS values pasted by users
        },
        "fontSize": {
            "options": [
                10,
                11,
                12,
                14,
                16,
                18,
                20,
                24,
                28,
                32,
                36,
                42,
                48,
                56,
                64,
                "default",
            ],
            "supportAllValues": True,
        },
        "fontColor": {
            "columns": 10,
            "documentColors": 24,
        },
        "fontBackgroundColor": {
            "columns": 10,
            "documentColors": 24,
        },
        # Headings
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
                {
                    "model": "heading4",
                    "view": "h4",
                    "title": "Heading 4",
                    "class": "ck-heading_heading4",
                },
                {
                    "model": "heading5",
                    "view": "h5",
                    "title": "Heading 5",
                    "class": "ck-heading_heading5",
                },
                {
                    "model": "heading6",
                    "view": "h6",
                    "title": "Heading 6",
                    "class": "ck-heading_heading6",
                },
            ]
        },
        # Lists
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        # Images
        "image": {
            "toolbar": [
                # نوار ابزار تصویر که هنگام انتخاب تصویر ظاهر می‌شود
                "imageTextAlternative",
                "toggleImageCaption",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:side",
                # موارد زیر مربوط به تنظیمات تصویر با متن است
                "imageStyle:alignLeft",
                "imageStyle:alignCenter",
                "imageStyle:alignRight",
                "linkImage",  # لینک دادن تصویر
            ],
        },
        # Tables
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": [
                    {"color": "hsl(0, 0%, 0%)", "label": "Black"},
                    {"color": "hsl(0, 0%, 30%)", "label": "Dim"},
                    {"color": "hsl(0, 0%, 60%)", "label": "Gray"},
                    {"color": "hsl(0, 0%, 90%)", "label": "Light"},
                ],
                "backgroundColors": [
                    {"color": "hsl(0, 0%, 100%)", "label": "White"},
                    {"color": "hsl(0, 0%, 90%)", "label": "Light"},
                    {"color": "hsl(60, 75%, 90%)", "label": "Yellow"},
                    {"color": "hsl(204, 70%, 90%)", "label": "Blue"},
                ],
            },
            "tableCellProperties": {
                "borderColors": [
                    {"color": "hsl(0, 0%, 0%)", "label": "Black"},
                    {"color": "hsl(0, 0%, 30%)", "label": "Dim"},
                    {"color": "hsl(0, 0%, 60%)", "label": "Gray"},
                    {"color": "hsl(0, 0%, 90%)", "label": "Light"},
                ],
                "backgroundColors": [
                    {"color": "hsl(0, 0%, 100%)", "label": "White"},
                    {"color": "hsl(0, 0%, 90%)", "label": "Light"},
                    {"color": "hsl(60, 75%, 90%)", "label": "Yellow"},
                    {"color": "hsl(204, 70%, 90%)", "label": "Blue"},
                ],
            },
        },
        # Media embed (optional previews)
        "mediaEmbed": {"previewsInData": True},
        # Code block languages
        "codeBlock": {
            "languages": [
                {"language": "plaintext", "label": "Plain text"},
                {"language": "bash", "label": "Bash"},
                {"language": "python", "label": "Python"},
                {"language": "javascript", "label": "JavaScript"},
                {"language": "typescript", "label": "TypeScript"},
                {"language": "json", "label": "JSON"},
                {"language": "yaml", "label": "YAML"},
                {"language": "html", "label": "HTML"},
                {"language": "css", "label": "CSS"},
                {"language": "scss", "label": "SCSS"},
                {"language": "java", "label": "Java"},
                {"language": "c", "label": "C"},
                {"language": "cpp", "label": "C++"},
                {"language": "php", "label": "PHP"},
                {"language": "ruby", "label": "Ruby"},
                {"language": "go", "label": "Go"},
                {"language": "rust", "label": "Rust"},
                {"language": "sql", "label": "SQL"},
            ]
        },
        # Optional autosave (requires Autosave plugin)
        "autosave": {"waitingTime": 3000},  # ms
        # Fine-tuning
        "removePlugins": [],
        "extraPlugins": [],
    }
}
