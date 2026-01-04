# 🐚 Nature Shell

> **A revolutionary shell scripting language based on parts of speech**  
> Designed and built by a 13-year-old developer

---

## 🌟 What makes Nature Shell special?

- **Natural Language Syntax**: Commands read like sentences
- **Type Safety**: Explicit type annotations prevent errors
- **Intuitive Design**: Based on linguistic parts of speech
- **Beginner Friendly**: Easy to learn, powerful to use

## 🚀 Quick Start

### Installation
```bash
# Coming soon
pip install nature-shell
```

### Your First Script
```bash
# Coming soon
# Create a variable
var:int crt $count -in 0

# Loop and print
$count < 5 -while {
    tmp echo "Count: $count"
    var ch $count -in $count + 1
}
```

### Try It Now
```bash
# Coming soon
python code/main.py
>>> var:str crt $name -in "World"
>>> tmp echo "Hello, $name"
Hello, World
>>> $age > 18 -if { tmp echo "Adult" }
Adult
```

## 💡 Why Nature Shell?

### Traditional Bash
```bash
if [ $usage -gt 80 ]; then
    echo "Out of memory"
else
    echo "Normal"
fi
```

### Nature Shell
```bash
$usage > 80 -if {
    echo "Out of memory"
} -else {
    echo "Normal"
}
```

**More readable. More intuitive. More natural.**

## 📖 The Story Behind Nature Shell

I'm a 13-year-old middle school student who got frustrated with traditional shell syntax. 

**The problem:** Bash, PowerShell, and other shells felt unintuitive and hard to remember.

**The solution:** What if commands followed natural language structure? What if we used parts of speech (nouns, verbs, adjectives) as a foundation?

That's how Nature Shell was born.

### Design Philosophy
- **Readability over brevity**: Code should read like sentences
- **Consistency over convention**: Everything follows the same rules
- **Safety over flexibility**: Types prevent silent errors

This is my first major project. I'm learning as I go, and I'd love your feedback! ⭐

## 🚧 Current Status

**This is a work in progress!** 

### ✅ Implemented
- [x] Variables (create, modify, retrieve)
- [x] Basic I/O (echo)
- [x] System commands
- [x] Error handling
- [x] REPL interface
- [x] Conditionals (-if, -else)
- [x] While Loop (-while) 

### 🔨 In Progress
- [ ] Foreach Loops (-foreach)
- [ ] Pipelines (|)
- [ ] Functions (fn def)
- [ ] Type checking

### 💭 Planned
- [ ] Standard library
- [ ] Package manager
- [ ] VSCode extension
- [ ] Documentation site

## 📚 Documentation

For detailed documentation, see [SPEC.md](docs/SPEC.md)

### Command Syntax
```
(Permission) (Noun)(:Adjective) (Verb)(!Adverb) (Value) (-Preposition) (Value)
```

### Examples
- [Basic Tutorial](examples/hello_world.ngs)
- [Advanced Usage](examples/advanced.md)

## 🎬 Demo

![Demo](https://via.placeholder.com/800x400?text=Demo+Coming+Soon)

*Terminal demo coming soon!*

## 🤝 Contributing

I'm a young developer learning as I go, and **your help would be amazing!**

### Ways to contribute:

- 🐛 Report bugs in [Issues](../../issues)
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star this repo (it really helps!)

**No contribution is too small!** Even fixing a typo helps.

## 💬 Contact

- GitHub Issues: [Report bugs or ask questions](../../issues)
- Email: hwangseonug12@gmail.com

## 🤖 Development Notes

This project was developed with AI assistance (Claude/ChatGPT).
- **Concept & Design**: Created by me
- **Implementation**: Built with AI pair programming
- **Learning Journey**: Continuously understanding and improving the code

I'm a 13-year-old developer learning through building!

---

**Made with ❤️ by a 13-year-old developer**

