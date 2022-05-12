# 3dpfl

https://the3dpfl.herokuapp.com

The 3d print failure library is a place to document, share, and browse 3d print failures and their solutions.

It is built with HTML, CSS, Python, Javascript, Flask, SQLAlchemy, and WTForms.

Users can post new entries to the library, with a description of the failure, the solution, and the printer and filament used. The printer and filament fields include an auto-complete feature, showing entries in the printer and filament tables that match what the user has typed. If the user enters a printer or filament that does not exist yet in the database, those values are added.

Users can also browse all entries, and filter by printer and filament type. Results are sorted by number of votes.

Users can vote for any post, including their own, to show support for that entry.
