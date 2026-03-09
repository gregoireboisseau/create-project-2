# Create Project

A Python script to quickly scaffold new web projects with your preferred framework. This tool streamlines the project setup process by handling Node.js version checks, framework selection, and initial configuration.

## Features

- ✅ **Node.js version check** - Ensures Node.js 20+ is installed (with nvm support)
- ✅ **Multiple framework support** - React, Next.js, Astro, Symfony, or empty project
- ✅ **Package manager choice** - npm, yarn, or pnpm
- ✅ **Automated setup** - Creates README, .gitignore, ESLint & Prettier configs (JS/TS projects only)
- ✅ **License selection** - MIT, Apache 2.0, GPL v3, or none
- ✅ **Auto-install dependencies** - Can install PHP, Composer for Symfony projects (with confirmation)

## Requirements

- **Python 3.10+** (for modern type hints support)
- **Node.js 20+** (will be checked automatically)
- **npm** (comes with Node.js, used to install yarn/pnpm if needed)

Optional dependencies based on framework choice:
- **nvm** - For automatic Node.js version management
- **Symfony CLI** or **Composer** - For Symfony projects (can be auto-installed)
- **PHP** - Required for Symfony (can be auto-installed on Ubuntu/Debian/macOS)

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/create-project.git
   cd create-project
   ```

2. Make the script executable:
   ```bash
   chmod +x create.py
   ```

## Usage

Run the script and follow the interactive prompts:

```bash
./create.py
```

### Project Types

1. **HTML/CSS (Empty)** - Creates a blank project structure, perfect for custom setups
2. **React** - Vite-based React application
   - Option for Single Page or Multi-page (with react-router-dom)
3. **Next.js** - Configurable Next.js application
   - Choose TypeScript, ESLint, Tailwind CSS, App Router, src/ directory, import aliases
4. **Astro** - Astro static site generator project
5. **Symfony** - PHP Symfony application
   - Uses Symfony CLI if available
   - Falls back to Composer (can be auto-installed)
   - PHP can be auto-installed on Ubuntu/Debian/macOS

### Package Manager

The script lets you choose between:
- **npm** - Standard Node.js package manager (recommended)
- **yarn** - Fast and reliable package manager
- **pnpm** - Fast, disk space efficient package manager

If your chosen package manager is not installed, the script offers to install it automatically.

### Interactive Prompts

The script will ask you for:
- Project name
- Package manager (npm/yarn/pnpm)
- Project type (framework)
- Framework-specific options (if applicable)
- Project description
- Author name
- License choice

### What Gets Created

For JavaScript/TypeScript projects:
```
your-project/
├── src/                 # Source files (framework-dependent)
├── .eslintrc.json       # ESLint configuration
├── .prettierrc          # Prettier configuration
├── .eslintignore        # ESLint ignore patterns
├── .prettierignore      # Prettier ignore patterns
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── LICENSE              # License file (if selected)
└── package.json         # Node.js dependencies
```

For Symfony projects:
```
your-project/
├── config/              # Symfony configuration
├── public/              # Web root
├── src/                 # PHP source files
├── templates/           # Twig templates
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── LICENSE              # License file (if selected)
├── composer.json        # PHP dependencies
└── symfony.lock         # Symfony lock file
```

## Example

```bash
$ ./create.py
==================================================
🚀 Create Project - Web project creation script
==================================================
✓ Using Node.js 20.11.0
📁 Project name: my-awesome-app

📦 Choose your package manager:
1) npm - Standard Node.js package manager (recommended)
2) yarn - Fast and reliable package manager
3) pnpm - Fast, disk space efficient package manager
→ Your choice [1-3]: 1

🌐 Project type:
1) HTML/CSS (empty project)
2) React
3) Next.js
4) Astro
5) Symfony
→ Your choice [1-5]: 2

⚛️  React application type:
1) Single Page Application
2) Multi-page with react-router-dom
→ Your choice [1-2]: 1

📝 Project description: My awesome React application
👤 Author name: John Doe

📄 License:
1) MIT
2) Apache 2.0
3) GPL v3
4) None
→ Your choice [1-4]: 1

⏳ Creating project...
⏳ Creating React project with Vite...
⚛️  React project created
✓ README.md file created
✓ .gitignore file created
✓ ESLint and Prettier configurations created
⏳ Installing ESLint and Prettier...
✓ ESLint and Prettier installed
✓ LICENSE file created

==================================================
🎉 Project 'my-awesome-app' is ready to code!
==================================================

To get started:
  cd /path/to/my-awesome-app
  npm run dev
```

## ESLint & Prettier Configuration

For JavaScript/TypeScript projects, the script creates ready-to-use configurations:

### ESLint Rules
- 2-space indentation
- Unix line endings
- Single quotes
- Semicolons required
- Warns on unused variables and console.log

### Prettier Rules
- Semicolons: enabled
- Single quotes
- Tab width: 2
- Trailing comma: ES5 style
- Print width: 100 characters

## Symfony Project Requirements

For Symfony projects, the script needs:
1. **PHP** (8.1+ recommended)
2. **Composer** (dependency manager)

If either is missing, the script will offer to install them automatically:
- **Ubuntu/Debian**: PHP installed via `apt` (with sudo confirmation)
- **macOS**: PHP installed via Homebrew (with confirmation)
- **Other systems**: Manual installation instructions provided

⚠️  **Note**: The script always asks for confirmation before running commands with `sudo`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Acknowledgments

Originally inspired by a Bash script, rewritten in Python for better stability and cross-platform compatibility.
