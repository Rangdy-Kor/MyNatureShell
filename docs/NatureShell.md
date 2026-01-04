# Nature Shell

# 1 Overview

NatureShell is the <mark style="background: #FFF3A3A6;">single official shell interface</mark> in AerogelOS responsible for system control, exercising permissions, and configuration automation.

Unlike traditional string-based shells, NatureShell treats all command input, output, and errors as objects, executing all control flow atop the Hub API and permission model.

# 2 Design Principles

NatureShell was designed based on the following principles:

- All targets are represented as **noun objects**
- All actions are performed only through **explicitly authorized commands**
- All data and errors are transmitted as **objects within pipes**
- Conditional checks and system modifications are **clearly separated**

Through this, NatureShell aims to be not just a shell for listing commands, but a <mark style="background: #FFF3A3A6;">language for describing systems</mark>.

All NatureShell commands execute via the Hub API. Thanks to the Hub API's asynchronous processing engine, even pipelines of multiple commands are handled efficiently.

# 3 Language Structure Overview

Existing shells rely on string pipes, where errors are handled outside the control flow.

NatureShell treats nouns as first-class objects, passing objects containing values, state, and errors through pipes.

In NatureShell, an object is the smallest executable unit identifiable by the kernel, directly connected to system components.

# 4 Command Syntax

NatureShell's basic commands follow this fixed structure:

`(Permission) (Noun)(:Adjective) (Verb) (!Adverb) (Value) (-Preposition) (Value)`

Each element is optional, but its position and role are strictly fixed.

# 5 Parts of Speech

NatureShell borrows natural language part-of-speech concepts but operates based on **structural roles** rather than semantic interpretation.

Each part of speech has a clear position and responsibility, prioritizing controllability over grammatical flexibility.

## 5.1 Comments

Though not a part of speech, comments can be marked by prefixing with //, ##, or cmt.

## 5.2 Permissions

> Refer to [[AerogelOS]]'s ACL (3.5.4) table.

Specifies the highest execution permission for the command. If omitted, it runs with user (default) permissions.

## 5.3 Noun

Specifies the target object on which the command acts.

## 5.4 Adjective

Defines detailed attributes of the noun. Starts with a colon (:) and follows immediately after the noun.

## 5.5 Verb

Specifies the action to be performed on the noun object. For comparative verbs, it is an expression with no side effects and returns a boolean object. This clearly separates conditional evaluation from system modification.

## 5.6 Adverb

Modifies how the verb is executed. Begins with ! and is placed immediately after the verb.

## 5.7 Value

> Read from [[AerogelOS]]'s virtual file system (/dev/)

Contains the actual data required by the command. Arithmetic expressions are permitted within the value section.

### 5.7.1 Arithmetic Expressions

- +: Addition
- -: Subtraction
- *: Multiplication
- /: Division
- %: Modulus
- **: Exponentiation

### 5.7.2 Automatic Variables

NatureShell exposes runtime state information as **automatic variables**. These automatic variables are structured under the single root object `$ctx`, and all items are **read-only system objects**.

`$ctx` cannot be created, deleted, or assigned by the user; it is dynamically bound by the kernel based on the execution context.

`$_` is provided as a <mark style="background: #FFF3A3A6;">read-only alias</mark> for `$ctx.pipeline.current` for the convenience of existing shell users. `$_` is only valid within pipeline or loop scopes. Outside these scopes, it returns a null object.

#### 5.7.2.1 `$ctx.process`

Represents the process and task unit currently executing the command.

- id : Process identifier
- parent : Parent process
- async : Indicates asynchronous execution
- thread : Execution thread information

#### 5.7.2.2 `$ctx.session`

Represents the current user session and working environment.

- id : Session identifier
- cwd : Current working directory
- user : Logged-in user object
- permission : Current valid permissions

#### 5.7.2.3 `$ctx.runtime`

Provides NatureShell and Hub API runtime information.

- shell_version
- hub_api_version
- os
- architecture

#### 5.7.2.4 `$ctx.pipeline`

Represents the pipeline execution state.

- current : Object currently being processed
- previous : Full output stream of the previous pipeline stage
- index : Pipeline stage index
- is_empty : Whether an input stream exists

#### 5.7.2.5 `$ctx.error`

Indicates error and exception states.

- last : The last error object that occurred
- stack : The error stack trace
- handled : Whether the most recent error was handled

### 5.7.3 Variable Rules

- Variables always start with $.
- Permitted characters: letters, numbers, underscore (_), hyphen (-).
- Cannot start with a number.
- Valid examples: $count, $user_name, $file-path

## 5.8 Prepositions

Connect values to specify execution context and relationships. Begin with a hyphen (-). -if targets the entire conditional expression completed by the preceding conjunction.

## 5.9 Conjunctions

Connect conditional expressions or commands for logical judgment. They start with - and, unlike prepositions, are followed by another conditional expression or command, not a value object.

# 6 Built-in Vocabulary

NatureShell embeds a minimal set of nouns and verbs necessary for system control.

This list is not a fixed API and can be extended via the Hub API and plugins.

## 6.1 Permissions

- root: Full system control permission.
- admin: Administrator permission.
- user: General user permission. Default when permission is omitted.

## 6.2 Nouns

- application/aplc/app: App object
- directory/dir: Directory path object
- file/fl: File object
- folder/fd: Folder object
- function/func/fn: Function object
- module/mod: Module object
- network/net: Network object
- system/sys: System and environment settings object
- tmp: Temporary object
- variable/var: Script variable

## 6.3 Adjectives

Data type

- array/arr
- bool
- byte/byt
- char/chr
- double/dou
- float/flo
- int
- list/ls
- long/lng
- map
- set
- short/sht
- string/str
- tuple/tup
  File extension
- bmp
- csv
- doc
- docx
- gif
- heic
- jpeg/jpe/jpg
- json
- m4a
- mkv
- mov
- mp3
- mp4
- png
- ppt
- pptx
- raw
- txt
- wav
- xls
- xlsx
- xml
- yaml
  Network
- ip
- port
- url
  Filtering
- memory/mem
- running/run
- service/svc
- size
- stopped/stp

## 6.4 Verbs

General Verbs

- append/apnd: Add/append data
- call: Call a function
- cast: Cast an object's data type
- change/chg/ch: Change a value
- convert/conv: Convert object extension
- create/crt: Create object
- def: Define function object
- echo: Output object
- get: Return found object
- list/ls: Return object list
- read/rd: Read data
- remove/rmv/rm: Remove object
- restart/rest: Restart service
- return/ret: Return specified object
- sort: Sort list
- start/strt: Start service
- stop/stp: Stop service
- swap/swp: Swap order/position of two objects
- write/wrt: Write/overwrite data
  Comparison verbs
- > : Greater than
  
- > =: Greater than or equal to
  
- <: Less than
- <=: Less than or equal to
- ==: Equal to
- !=: Not equal to

## 6.5 Adverbs

- !asce: Ascending order
- !async: Asynchronous execution
- !background/!back
- !delay/!dly: Execute after delay
- !desc: Descending order
- !force/!frc: Force execution
- !question/!qst: Execute after confirmation
- !recurse/!rcs: Recursive function

## 6.6 Prepositions

- -if {}: if ~
- -else {}: otherwise
- -foreach {}/-for {}: repeat for each occurrence
- -while {}/whl {}: repeat while condition holds
- -catch {}/-cat {}: exception/error handling
- -connect/-conc {}: Connect to external system
- -until/-unt {}: Wait until specific condition
- -by: By ~ amount
- -in: In ~ state
- -of: Of ~ (possessive)
- -quality/-qual: Quality
- -to: To
- -wi/-with: With

## 6.7 Conjunctions

- -and/-a: And (logical AND)
- -or/-o: Or (logical OR)
- -not/-n: Not (logical negation)

### 6.7.1 Priority

1. -not (highest priority)
2. -and
3. -or (lowest priority)

Explicit priority can be specified using parentheses ()

Example: ($cpu > 80 -and $mem > 80) -or $emergency_mode

# 7 Usage Examples

The following examples demonstrate that NatureShell is not merely a simple automation script, but a <mark style="background: #FFF3A3A6;">language for describing system state</mark>.

## 7.1 Creating Variables

```
var:int crt $age -in 25
var:str crt $name -in “John”
var:list crt $items -in [1, 2, 3]
```

## 7.2 File Operations

```
dir ch C:/path
file crt test.txt -in “Hello, World!”
file:txt ls!rcs C:/home/user
root fd rm!frc c:/path
```

## 7.3 Conditional Execution

```
sys:mem get | var:int crt $usage -in $_
$usage > 80 -if {
    echo “Out of memory”
} -else {
    echo “Normal”
}
```

## 7.4 Loops

```
file:txt ls | -foreach {
    echo “File: $_ ”
}

var:int crt $i -in 0
$i < 10 -while {
    echo $i
    var ch $i -in $i + 1
}
```

## 7.5 Pipeline Chaining

```
file:log ls |
    file:size[^1] sort -desc |
    var:list crt $top5 -in $_ |
    echo $_
```

## 7.6 System Manipulation

```
root fd rm!frt c:path
```

## 7.7 Practical Examples

### 7.7.1 Backup Script

```
sys:date get -format “%Y%m%d” | var:str crt $today -in $_
file:log ls!rcs /var/logs |
    -foreach {
        file copy $_ -to /backup/$today/$_
     }
```

### 7.7.2 System Monitoring

```
sys:cpu get | var:int crt $cpu -in $_
sys:mem get | var:int crt $mem -in $_

$cpu > 80 -and $mem > 80 -if {
     echo “System overload!”
     sys:serv rest high-usage-app
} -else {
    echo “System normal”
}
```

### 7.7.3 Delete Temporary Files Older Than 30 Days

```
file:tmp ls /temp |
    file:age > 30d -if {
        file rm!frc $_
    }
```

### 7.7.4 Batch Image Conversion

```
file:jpg ls /photos |
    -foreach {
        file conv $_ -to png -qual 90
        echo “Conversion complete: $_ ”
    }
```

### 7.7.5 Function Definition and Usage

```
fn def create-backup-dir ($format) {
    sys:date get -format $format | var:str crt $date-path -in $_
    dir crt /backup/$date-path -cat {
        tmp echo “Error: Could not create backup directory.”
        ret false
    }
    ret /backup/$date-path
}

fn call create-backup-dir -with “%Y%m%d” | var:str crt $today-dir -in $_

$today-dir != false -if {
    echo “Backup directory created successfully: $today-dir”
} -else {
    echo “Script terminated: Backup failed. ”
}
```

1

file:size is a file object stream based on attributes.
