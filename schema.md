users
 - id
 - username
 - password

filaments
 - id
 - brand
 - type

printers
 - id
 - brand
 - model

post
 - id
 - user_id
 - printer_modified (yes/no)
 - printer_id --> printer models
 - filament_id --> filaments
 - failure description
 - solution description
 - image


comment
 - id
 - user_id --> users
 - post_id --> posts
 - comment

vote
 - id
 - user_id --> users
 - post_id --> posts

tag
 - id
 - name

post_tags
 - post_id --> posts 
 - tag_id --> tags
