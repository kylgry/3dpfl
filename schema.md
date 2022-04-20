users
 - username
 - password

filament brands
 - id
 - brand

filaments
 - id
 - brand (--> filament brands)
 - type

printer brands
 - id
 - brand

printers
 - id
 - brand (--> printer brands)
 - model

failure categories
 - id
 - name

 post
  - id
  - failure category (--> failure category)
  - printer model (--> printer models)
  - filament name (--> filaments)
  - failure description
  - solution description
  - image

comment
 - id
 - username
 - comment

vote
 - username (primary key)
 - post (primary key)
