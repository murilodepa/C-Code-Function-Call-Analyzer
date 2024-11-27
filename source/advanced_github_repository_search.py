import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

params2 = {}

def toggle_exclude_forks():
    var_only_forks.set(False)

def toggle_only_forks():
    var_exclude_forks.set(False)

def search_repositories():
    global params2
    query = []
    name = entry_name.get()
    selected_license = combobox_license.get()
    selected_topic = combobox_topic.get()
    selected_language = combobox_language.get()
    selected_label = combobox_label.get()
    
    commits_min = entry_commits_min.get()
    commits_max = entry_commits_max.get()
    contrib_min = entry_contrib_min.get()
    contrib_max = entry_contrib_max.get()
    issues_min = entry_issues_min.get()
    issues_max = entry_issues_max.get()
    prs_min = entry_prs_min.get()
    prs_max = entry_prs_max.get()
    branches_min = entry_branches_min.get()
    branches_max = entry_branches_max.get()
    releases_min = entry_releases_min.get()
    releases_max = entry_releases_max.get()
    
    date_created_min = entry_date_created_min.get()
    date_created_max = entry_date_created_max.get()
    date_last_commit_min = entry_date_last_commit_min.get()
    date_last_commit_max = entry_date_last_commit_max.get()
    
    stars_min = entry_stars_min.get()
    stars_max = entry_stars_max.get()
    watchers_min = entry_watchers_min.get()
    watchers_max = entry_watchers_max.get()
    forks_min = entry_forks_min.get()
    forks_max = entry_forks_max.get()
    
    nblines_min = entry_nblines_min.get()
    nblines_max = entry_nblines_max.get()
    code_lines_min = entry_code_lines_min.get()
    code_lines_max = entry_code_lines_max.get()
    comment_lines_min = entry_comment_lines_min.get()
    comment_lines_max = entry_comment_lines_max.get()

    sorting_by = combobox_sorting_by.get()
    sorting_order = combobox_sorting_order.get()

    selected_options = []
    
    if name:
        selected_options.append(f"Name: {name}")
    if selected_license and selected_license != "Select a License":
        selected_options.append(f"License: {selected_license}")
        query.append(f"license:{selected_license}")
    if selected_topic and selected_topic != "Has topic":
        selected_options.append(f"Topic: {selected_topic}")
        query.append(f"topic:{selected_topic}")
    if selected_language and selected_language != "Language":
        selected_options.append(f"Language: {selected_language}")
        query.append(f"language:{selected_language}")
    if selected_label and selected_label != "Uses Label":
        selected_options.append(f"Uses Label: {selected_label}")
        query.append(f"label:{selected_label}")

    if commits_min or commits_max:
        selected_options.append(f"Commits: {commits_min} - {commits_max}")
        if commits_min:
            query.append(f"commits:>{commits_min}")
        if commits_max:
            query.append(f"commits:<{commits_max}")

    if contrib_min or contrib_max:
        selected_options.append(f"Contributors: {contrib_min} - {contrib_max}")
        if contrib_min:
            query.append(f"contributors:>{contrib_min}")
        if contrib_max:
            query.append(f"contributors:<{contrib_max}")

    if issues_min or issues_max:
        selected_options.append(f"Issues: {issues_min} - {issues_max}")
        if issues_min:
            query.append(f"open_issues:>{issues_min}")
        if issues_max:
            query.append(f"open_issues:<{issues_max}")

    if prs_min or prs_max:
        selected_options.append(f"Pull Requests: {prs_min} - {prs_max}")
        if prs_min:
            query.append(f"pull_requests:>{prs_min}")
        if prs_max:
            query.append(f"pull_requests:<{prs_max}")

    if branches_min or branches_max:
        selected_options.append(f"Branches: {branches_min} - {branches_max}")
        if branches_min:
            query.append(f"branches:>{branches_min}")
        if branches_max:
            query.append(f"branches:<{branches_max}")

    if releases_min or releases_max:
        selected_options.append(f"Releases: {releases_min} - {releases_max}")
        if releases_min:
            query.append(f"releases:>{releases_min}")
        if releases_max:
            query.append(f"releases:<{releases_max}")

    if date_created_min or date_created_max:
        selected_options.append(f"Created between: {date_created_min} - {date_created_max}")
        if date_created_min:
            query.append(f"created:>{date_created_min}")
        if date_created_max:
            query.append(f"created:<{date_created_max}")
    
    if date_last_commit_min or date_last_commit_max:
        selected_options.append(f"Last commit between: {date_last_commit_min} - {date_last_commit_max}")
        if date_last_commit_min:
            query.append(f"pushed:>{date_last_commit_min}")
        if date_last_commit_max:
            query.append(f"pushed:<{date_last_commit_max}")

    if stars_min or stars_max:
        selected_options.append(f"Stars: {stars_min} - {stars_max}")
        if stars_min:
            query.append(f"stars:>{stars_min}")
        if stars_max:
            query.append(f"stars:<{stars_max}")

    if watchers_min or watchers_max:
        selected_options.append(f"Watchers: {watchers_min} - {watchers_max}")
        if watchers_min:
            query.append(f"watchers:>{watchers_min}")
        if watchers_max:
            query.append(f"watchers:<{watchers_max}")

    if forks_min or forks_max:
        selected_options.append(f"Forks: {forks_min} - {forks_max}")
        if forks_min:
            query.append(f"forks:>{forks_min}")
        if forks_max:
            query.append(f"forks:<{forks_max}")

    if nblines_min or nblines_max:
        selected_options.append(f"Non Blank Lines: {nblines_min} - {nblines_max}")
        if nblines_min:
            query.append(f"non_blank_lines:>{nblines_min}")
        if nblines_max:
            query.append(f"non_blank_lines:<{nblines_max}")
    
    if code_lines_min or code_lines_max:
        selected_options.append(f"Code Lines: {code_lines_min} - {code_lines_max}")
        if code_lines_min:
            query.append(f"code_lines:>{code_lines_min}")
        if code_lines_max:
            query.append(f"code_lines:<{code_lines_max}")

    if comment_lines_min or comment_lines_max:
        selected_options.append(f"Comment Lines: {comment_lines_min} - {comment_lines_max}")
        if comment_lines_min:
            query.append(f"comment_lines:>{comment_lines_min}")
        if comment_lines_max:
            query.append(f"comment_lines:<{comment_lines_max}")

    # Sorting
    if sorting_by:
        selected_options.append(f"Sorting by: {sorting_by}")
        query.append(f"sort:{sorting_by}")

    if sorting_order:
        selected_options.append(f"Sorting order: {sorting_order}")
        query.append(f"order:{sorting_order}")

    # Checkboxes
    if var_exclude_forks.get():
        selected_options.append("Exclude Forks")
        query.append("fork:false") 
    if var_only_forks.get():
        selected_options.append("Only Forks")
        query.append("fork:true") 
    if var_has_wiki.get():
        selected_options.append("Has Wiki")
        query.append("has_wiki:true")
    if var_has_license.get():
        selected_options.append("Has License")
        query.append("has_license:true")
    if var_has_open_issues.get():
        selected_options.append("Has Open Issues")
        query.append("open_issues:true")
    if var_has_pull_requests.get():
        selected_options.append("Has Pull Requests")
        query.append("pull_requests:true")

    # Displays the selected options
    if selected_options:
        selected_options_str = "\n".join(selected_options)
        messagebox.showinfo("Search", f"Search conducted with the following parameters:\n{selected_options_str}")
    else:
        messagebox.showinfo("Search", "No options selected for search.")
    window.destroy()
    
    params2 = {
        "q": " ".join(query),
        "sort": sorting_by if sorting_by else "updated",
        "order": sorting_order if sorting_order else "desc",
        "per_page": 30,
        "page": 1
    }
    return params2

# Main Window Configuration
window = tk.Tk()
window.title("Advanced Repository Search on GitHub")
window.geometry("500x850")

# Creation of the canvas and the frame
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configuring the frame to be scrollable
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Placing the canvas and the scrollbar in the window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# General Section
tk.Label(scrollable_frame, text="General", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)

# Search by keyword in name (Contains)
frame_nome = tk.Frame(scrollable_frame)
frame_nome.pack(anchor="w", pady=5)
tk.Label(frame_nome, text="Search by keyword in name (Contains):").grid(row=0, column=0, padx=(0, 5))
entry_name = tk.Entry(frame_nome, width=40)
entry_name.grid(row=0, column=1)

# License
frame_license = tk.Frame(scrollable_frame)
frame_license.pack(anchor="w", pady=5)
tk.Label(frame_license, text="Select a License:").grid(row=0, column=0, padx=(0, 5))
licenses = [
    "MIT License", "Apache License 2.0", "Other", "GNU General Public License", 
    "BSD 3-Clause New or Revised License", "GNU General Public License v2.0",
    "GNU Affero General Public License v3.0", "BSD 2-Clause Simplified License",
    "GNU Lesser General Public License v3.0", "Mozilla Public License 2.0"
]
combobox_license = ttk.Combobox(frame_license, values=licenses, state="readonly", width=35)
combobox_license.set("Select a License")
combobox_license.grid(row=0, column=1)

# Has Topic
frame_topico = tk.Frame(scrollable_frame)
frame_topico.pack(anchor="w", pady=5)
tk.Label(frame_topico, text="Has topic:").grid(row=0, column=0, padx=(0, 5))
combobox_topic = ttk.Combobox(frame_topico, values=["C", "CPP"], state="readonly", width=35)
combobox_topic.set("Has topic")
combobox_topic.grid(row=0, column=1)

# Language
frame_linguagem = tk.Frame(scrollable_frame)
frame_linguagem.pack(anchor="w", pady=5)
tk.Label(frame_linguagem, text="Language:").grid(row=0, column=0, padx=(0, 5))
combobox_language = ttk.Combobox(frame_linguagem, values=["C", "C++", "C#"], state="readonly", width=35)
combobox_language.set("Language")
combobox_language.grid(row=0, column=1)

# Label
frame_label = tk.Frame(scrollable_frame)
frame_label.pack(anchor="w", pady=5)
tk.Label(frame_label, text="Uses Label:").grid(row=0, column=0, padx=(0, 5))
labels = ["bug", "duplicate", "question", "enhancement", "wontfix", "invalid", "help wanted", 
          "good first issue", "documentation", "dependencies"]
combobox_label = ttk.Combobox(frame_label, values=labels, state="readonly", width=35)
combobox_label.set("Uses Label")
combobox_label.grid(row=0, column=1)

# History and Activity Section
tk.Label(scrollable_frame, text="History and Activity", font=("Arial", 11, "bold")).pack(anchor="w", pady=10)

# Function to create min and max field pairs in a single line
def add_range_field(label, parent):
    frame = tk.Frame(parent)
    frame.pack(anchor="w", pady=5)
    tk.Label(frame, text=label).grid(row=0, column=0)
    min_entry = tk.Entry(frame, width=10)
    min_entry.grid(row=0, column=1, padx=5)
    max_entry = tk.Entry(frame, width=10)
    max_entry.grid(row=0, column=2, padx=5)
    return min_entry, max_entry

entry_commits_min, entry_commits_max = add_range_field("Commits", scrollable_frame)
entry_contrib_min, entry_contrib_max = add_range_field("Contributors", scrollable_frame)
entry_issues_min, entry_issues_max = add_range_field("Issues", scrollable_frame)
entry_prs_min, entry_prs_max = add_range_field("Pull Requests", scrollable_frame)
entry_branches_min, entry_branches_max = add_range_field("Branches", scrollable_frame)
entry_releases_min, entry_releases_max = add_range_field("Releases", scrollable_frame)

# Date-based
tk.Label(scrollable_frame, text="Date-based Filters", font=("Arial", 11, "bold")).pack(anchor="w", pady=10)
entry_date_created_min, entry_date_created_max = add_range_field("Created between", scrollable_frame)
entry_date_last_commit_min, entry_date_last_commit_max = add_range_field("Last commit between", scrollable_frame)

# Popularity Filters
tk.Label(scrollable_frame, text="Popularity Filters", font=("Arial", 11, "bold")).pack(anchor="w", pady=10)
entry_stars_min, entry_stars_max = add_range_field("Stars", scrollable_frame)
entry_watchers_min, entry_watchers_max = add_range_field("Watchers", scrollable_frame)
entry_forks_min, entry_forks_max = add_range_field("Forks", scrollable_frame)

# Size of Codebase
tk.Label(scrollable_frame, text="Size of Codebase", font=("Arial", 11, "bold")).pack(anchor="w", pady=10)
entry_nblines_min, entry_nblines_max = add_range_field("Non Blank Lines", scrollable_frame)
entry_code_lines_min, entry_code_lines_max = add_range_field("Code Lines", scrollable_frame)
entry_comment_lines_min, entry_comment_lines_max = add_range_field("Comment Lines", scrollable_frame)

# Additional Filters
tk.Label(scrollable_frame, text="Additional Filters", font=("Arial", 11, "bold")).pack(anchor="w", pady=10)
tk.Label(scrollable_frame, text="Sorting by").pack(anchor="w")
combobox_sorting_by = ttk.Combobox(scrollable_frame, values=["Name", "Commit", "Contributors", "Issues", "Pull Requests", 
                                                   "Branches", "Stars", "Watchers", "Forks", "Created At", 
                                                   "Update At", "Last Commit"], state="readonly")
combobox_sorting_by.pack(pady=5)
combobox_sorting_order = ttk.Combobox(scrollable_frame, values=["Ascending", "Descending"], state="readonly")
combobox_sorting_order.pack(pady=5)

# Checkboxes
var_exclude_forks = tk.BooleanVar()
var_only_forks = tk.BooleanVar()
var_has_wiki = tk.BooleanVar()
var_has_license = tk.BooleanVar()
var_has_open_issues = tk.BooleanVar()
var_has_pull_requests = tk.BooleanVar()

tk.Checkbutton(scrollable_frame, text="Exclude Forks", variable=var_exclude_forks, command=toggle_exclude_forks).pack(anchor="w")
tk.Checkbutton(scrollable_frame, text="Only Forks", variable=var_only_forks, command=toggle_only_forks).pack(anchor="w")
tk.Checkbutton(scrollable_frame, text="Has Wiki", variable=var_has_wiki).pack(anchor="w")
tk.Checkbutton(scrollable_frame, text="Has License", variable=var_has_license).pack(anchor="w")
tk.Checkbutton(scrollable_frame, text="Has Open Issues", variable=var_has_open_issues).pack(anchor="w")
tk.Checkbutton(scrollable_frame, text="Has Pull Requests", variable=var_has_pull_requests).pack(anchor="w")

# Search button
search_button = tk.Button(scrollable_frame, text="Search", command=search_repositories)
search_button.pack(pady=20)

# Adjust the width of the text entry field
for entry in [entry_name, entry_commits_min, entry_commits_max,
               entry_contrib_min, entry_contrib_max, entry_issues_min, 
               entry_issues_max, entry_prs_min, entry_prs_max, 
               entry_branches_min, entry_branches_max, entry_releases_min, 
               entry_releases_max, entry_date_created_min, entry_date_created_max,
               entry_date_last_commit_min, entry_date_last_commit_max,
               entry_stars_min, entry_stars_max, entry_watchers_min, 
               entry_watchers_max, entry_forks_min, entry_forks_max, 
               entry_nblines_min, entry_nblines_max, entry_code_lines_min, 
               entry_code_lines_max, entry_comment_lines_min, entry_comment_lines_max]:
    entry.config(width=15)

window.mainloop()