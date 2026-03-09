#!/usr/bin/env python3
"""Web project creation script - React, Next.js, Astro, Symfony, or empty."""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    """Execute a shell command and return the result."""
    return subprocess.run(cmd, cwd=cwd, capture_output=False)


def check_node_version() -> tuple[bool, str]:
    """Check if Node.js 20+ is installed. Returns (success, version)."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, ""
        version = result.stdout.strip().lstrip("v")
        major = int(version.split(".")[0])
        return major >= 20, version
    except (FileNotFoundError, ValueError):
        return False, ""


def has_nvm() -> bool:
    """Check if nvm is available."""
    nvm_dir = os.environ.get("NVM_DIR")
    if not nvm_dir:
        return False
    return os.path.isfile(os.path.join(nvm_dir, "nvm.sh"))


def install_node_via_nvm(version: int) -> bool:
    """Install Node.js via nvm."""
    print(f"⏳ Installing Node.js {version} via nvm...")
    result = subprocess.run(["bash", "-c", f"source $NVM_DIR/nvm.sh && nvm install {version}"])
    return result.returncode == 0


def use_node_via_nvm(version: int) -> bool:
    """Use the specified Node.js version via nvm."""
    result = subprocess.run(["bash", "-c", f"source $NVM_DIR/nvm.sh && nvm use {version}"])
    return result.returncode == 0


def ensure_node_version() -> bool:
    """Ensure Node.js 20+ is available."""
    NODE_REQUIRED = 20

    success, version = check_node_version()
    if success:
        print(f"✓ Using Node.js {version}")
        return True

    # Node.js missing or version too old
    if has_nvm():
        print(f"⚠️  Node.js {NODE_REQUIRED}+ required (found {version or 'none'}).")
        print(f"🔍 nvm detected. Would you like to use Node.js {NODE_REQUIRED}? (y/n)")
        response = input("→ ").strip().lower()

        if response in ("y", "yes"):
            # Check if Node 20 is already installed
            check_result = subprocess.run(
                ["bash", "-c", f"source $NVM_DIR/nvm.sh && nvm ls --no-colors | grep -q 'v{NODE_REQUIRED}'"],
                capture_output=True
            )

            if check_result.returncode == 0:
                print(f"✓ Node.js {NODE_REQUIRED} found in nvm")
                if use_node_via_nvm(NODE_REQUIRED):
                    print(f"✓ Switched to Node.js {NODE_REQUIRED}")
                    return True
            else:
                print(f"🔧 Node.js {NODE_REQUIRED} is not installed via nvm. Would you like to install it? (y/n)")
                response = input("→ ").strip().lower()
                if response in ("y", "yes"):
                    if install_node_via_nvm(NODE_REQUIRED):
                        print(f"✓ Node.js {NODE_REQUIRED} installed and activated")
                        return True

        print(f"❌ Node.js {NODE_REQUIRED}+ is required. Please install it manually.")
        sys.exit(1)
    else:
        if not version:
            print(f"❌ Node.js is not installed.")
        else:
            print(f"❌ Node.js version {version} is not supported.")
        print(f"Please install Node.js version {NODE_REQUIRED} or higher, or install nvm.")
        print("- Download Node.js: https://nodejs.org/")
        print("- Install nvm: https://github.com/nvm-sh/nvm#installing-and-updating")
        sys.exit(1)

    return False


def get_project_name() -> str:
    """Prompt for project name."""
    while True:
        name = input("📁 Project name: ").strip()
        if name:
            return name
        print("❌ Project name cannot be empty.")


def get_project_type() -> str:
    """Display project type selection menu."""
    print("\n🌐 Project type:")
    print("1) HTML/CSS (empty project)")
    print("2) React")
    print("3) Next.js")
    print("4) Astro")
    print("5) Symfony")

    while True:
        choice = input("→ Your choice [1-5]: ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("❌ Invalid option. Please try again.")


def get_react_type() -> str:
    """Prompt for React application type."""
    print("\n⚛️  React application type:")
    print("1) Single Page Application")
    print("2) Multi-page with react-router-dom")

    while True:
        choice = input("→ Your choice [1-2]: ").strip()
        if choice in ("1", "2"):
            return choice
        print("❌ Invalid option. Please try again.")


def get_nextjs_options() -> dict:
    """Prompt for Next.js options."""
    print("\n⚡ Next.js options:")

    options = {
        "typescript": False,
        "eslint": False,
        "tailwind": False,
        "app": False,
        "src_dir": False,
        "import_alias": False,
    }

    for key, label in [
        ("typescript", "TypeScript"),
        ("eslint", "ESLint"),
        ("tailwind", "Tailwind CSS"),
        ("app", "App Router (instead of Pages Router)"),
        ("src_dir", "src/ directory"),
        ("import_alias", "Import alias (@/*)"),
    ]:
        while True:
            response = input(f"→ Do you want {label}? (y/n): ").strip().lower()
            if response in ("y", "yes"):
                options[key] = True
                break
            elif response in ("n", "no"):
                options[key] = False
                break
            print("❌ Invalid response. Please answer with 'y' or 'n'.")

    return options


def get_description() -> str:
    """Prompt for project description."""
    return input("\n📝 Project description: ").strip()


def get_author() -> str:
    """Prompt for author name."""
    while True:
        author = input("👤 Author name: ").strip()
        if author:
            return author
        print("❌ Author name cannot be empty.")


def get_license() -> str | None:
    """Prompt for project license."""
    print("\n📄 License:")
    print("1) MIT")
    print("2) Apache 2.0")
    print("3) GPL v3")
    print("4) None")

    while True:
        choice = input("→ Your choice [1-4]: ").strip()
        if choice in ("1", "2", "3", "4"):
            return choice
        print("❌ Invalid option. Please try again.")


def create_license(choice: str, author: str) -> None:
    """Create LICENSE file based on choice."""
    year = datetime.now().year

    licenses = {
        "1": f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
        "2": f"""Copyright (c) {year} {author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""",
        "3": f"""Copyright (c) {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
""",
    }

    if choice in licenses:
        with open("LICENSE", "w") as f:
            f.write(licenses[choice])
        print("✓ LICENSE file created")
    else:
        print("ℹ️  No license added")


def create_eslint_prettier_config() -> None:
    """Create useful configurations for ESLint and Prettier."""
    # ESLint config
    eslint_config = """{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": ["eslint:recommended"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "indent": ["error", 2],
    "linebreak-style": ["error", "unix"],
    "quotes": ["error", "single"],
    "semi": ["error", "always"],
    "no-unused-vars": "warn",
    "no-console": "warn"
  }
}
"""

    # Prettier config
    prettier_config = """{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "always"
}
"""

    # ESLint ignore
    eslint_ignore = """node_modules
dist
.next
build
coverage
*.min.js
"""

    # Prettier ignore
    prettier_ignore = """node_modules
dist
.next
build
coverage
*.min.js
"""

    with open(".eslintrc.json", "w") as f:
        f.write(eslint_config)

    with open(".prettierrc", "w") as f:
        f.write(prettier_config)

    with open(".eslintignore", "w") as f:
        f.write(eslint_ignore)

    with open(".prettierignore", "w") as f:
        f.write(prettier_ignore)

    print("✓ ESLint and Prettier configurations created")


def create_gitignore() -> None:
    """Create a comprehensive .gitignore file."""
    gitignore = """# Dependencies
node_modules/
.pnp
.pnp.js

# Build outputs
dist/
build/
.next/
out/

# Vite
.vite/

# Environment variables
.env
.env.local
.env.*.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
coverage/

# Misc
.cache/
.temp/
"""

    with open(".gitignore", "w") as f:
        f.write(gitignore)

    print("✓ .gitignore file created")


def create_readme(project_name: str, description: str) -> None:
    """Create README.md file."""
    readme = f"""# {project_name}

{description}

## Installation

```bash
npm install
```

## Getting Started

```bash
npm run dev
```
"""

    with open("README.md", "w") as f:
        f.write(readme)

    print("✓ README.md file created")


def create_empty_project(project_name: str) -> None:
    """Create an empty project."""
    os.makedirs(project_name)
    os.chdir(project_name)
    print(f"📁 Empty project '{project_name}' created")


def create_react_project(project_name: str, react_type: str) -> None:
    """Create a React project with Vite."""
    print("⏳ Creating React project with Vite...")
    run_command(["npm", "create", "vite@latest", project_name, "--", "--template", "react"])
    os.chdir(project_name)
    print("⚛️  React project created")

    if react_type == "2":
        print("⏳ Installing react-router-dom...")
        run_command(["npm", "install", "react-router-dom"])

        # Create directory structure
        os.makedirs("src/pages", exist_ok=True)
        os.makedirs("src/routes", exist_ok=True)

        # Home.jsx
        with open("src/pages/Home.jsx", "w") as f:
            f.write("""export default function Home() {
  return <h1>Home</h1>;
}
""")

        # Contact.jsx
        with open("src/pages/Contact.jsx", "w") as f:
            f.write("""export default function Contact() {
  return <h1>Contact</h1>;
}
""")

        # About.jsx
        with open("src/pages/About.jsx", "w") as f:
            f.write("""export default function About() {
  return <h1>About</h1>;
}
""")

        # routes.jsx
        with open("src/routes/routes.jsx", "w") as f:
            f.write("""import { createBrowserRouter } from 'react-router-dom';
import Home from '../pages/Home';
import Contact from '../pages/Contact';
import About from '../pages/About';

const router = createBrowserRouter([
  { path: '/', element: <Home /> },
  { path: '/contact', element: <Contact /> },
  { path: '/about', element: <About /> },
]);

export default router;
""")

        print("✓ Multi-page structure created with react-router-dom")


def create_nextjs_project(project_name: str, options: dict) -> None:
    """Create a Next.js project with specified options."""
    print("⏳ Creating Next.js project...")

    cmd = ["npx", "create-next-app@latest", project_name]

    # Add flags based on options
    if options["typescript"]:
        cmd.append("--typescript")
    if options["eslint"]:
        cmd.append("--eslint")
    if options["tailwind"]:
        cmd.append("--tailwind")
    if options["app"]:
        cmd.append("--app")
    if options["src_dir"]:
        cmd.append("--src-dir")
    if options["import_alias"]:
        cmd.extend(["--import-alias", "@/*"])

    run_command(cmd)
    os.chdir(project_name)

    print("⚡ Next.js project created")


def create_astro_project(project_name: str) -> None:
    """Create an Astro project."""
    print("⏳ Creating Astro project...")
    run_command(["npm", "create", "astro@latest", project_name])
    os.chdir(project_name)
    print("🚀 Astro project created")


def has_php() -> bool:
    """Check if PHP is available."""
    try:
        result = subprocess.run(["php", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_php_ubuntu() -> bool:
    """Install PHP on Ubuntu/Debian systems."""
    print("⏳ Installing PHP...")
    result = subprocess.run(
        ["bash", "-c", "sudo apt update && sudo apt install -y php php-cli php-mbstring php-xml php-curl php-zip"]
    )
    return result.returncode == 0


def install_php_macos() -> bool:
    """Install PHP on macOS using Homebrew."""
    print("⏳ Installing PHP via Homebrew...")
    result = subprocess.run(["brew", "install", "php"])
    return result.returncode == 0


def install_php() -> bool:
    """Install PHP based on the operating system."""
    import platform

    system = platform.system()

    if system == "Linux":
        # Try to detect package manager
        if os.path.isfile("/etc/debian_version") or os.path.isfile("/usr/bin/apt"):
            return install_php_ubuntu()
        elif os.path.isfile("/etc/redhat-release") or os.path.isfile("/usr/bin/dnf"):
            print("ℹ️  RHEL/CentOS detected. Please install PHP manually:")
            print("   sudo dnf install php php-cli php-mbstring php-xml php-curl")
            return False
        else:
            print("ℹ️  Unknown Linux distribution. Please install PHP manually.")
            return False
    elif system == "Darwin":  # macOS
        # Check if Homebrew is installed
        try:
            result = subprocess.run(["brew", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return install_php_macos()
        except FileNotFoundError:
            pass
        print("ℹ️  Homebrew not installed. Please install PHP manually or install Homebrew first.")
        print("   https://brew.sh/")
        return False
    else:
        print(f"ℹ️  Unsupported OS ({system}). Please install PHP manually.")
        return False


def has_composer() -> bool:
    """Check if Composer is available."""
    try:
        result = subprocess.run(["composer", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_composer() -> bool:
    """Install Composer globally."""
    print("⏳ Installing Composer...")
    # Download and install Composer with sudo for the move operation
    result = subprocess.run(
        ["bash", "-c", "curl -sS https://getcomposer.org/installer | php && sudo mv composer.phar /usr/local/bin/composer"]
    )
    return result.returncode == 0


def create_symfony_project(project_name: str) -> None:
    """Create a Symfony project."""
    print("⏳ Creating Symfony project...")

    # Check if Symfony CLI is available
    try:
        result = subprocess.run(["symfony", "--version"], capture_output=True, text=True)
        has_symfony = result.returncode == 0
    except FileNotFoundError:
        has_symfony = False

    if has_symfony:
        run_command(["symfony", "new", project_name, "--webapp"])
        os.chdir(project_name)
        print("🎻 Symfony project created with Symfony CLI")
        return

    # Symfony CLI not available, check for PHP and Composer
    if not has_php():
        print("ℹ️  PHP is not installed.")
        print("🔧 Would you like to install PHP? (y/n)")
        response = input("→ ").strip().lower()

        if response in ("y", "yes"):
            if install_php():
                print("✓ PHP installed successfully")
                # Reload PHP check
                if not has_php():
                    print("⚠️  PHP installation may require restarting your terminal.")
                    print("Please restart your terminal and run Composer installation manually.")
                    sys.exit(1)
            else:
                print("❌ Failed to install PHP automatically.")
                print("Please install PHP manually: https://www.php.net/manual/en/install.php")
                sys.exit(1)
        else:
            print("❌ PHP is required to create a Symfony project.")
            print("Please install PHP: https://www.php.net/manual/en/install.php")
            sys.exit(1)

    if not has_composer():
        print("ℹ️  Composer is not installed.")
        print("🔧 Would you like to install Composer? (y/n)")
        response = input("→ ").strip().lower()

        if response in ("y", "yes"):
            if install_composer():
                print("✓ Composer installed successfully")
            else:
                print("❌ Failed to install Composer automatically.")
                print("Please install Composer manually: https://getcomposer.org/download/")
                sys.exit(1)
        else:
            print("❌ Composer is required to create a Symfony project.")
            print("Please install Composer: https://getcomposer.org/download/")
            sys.exit(1)

    # Create Symfony project with Composer
    run_command(["composer", "create-project", "symfony/skeleton", project_name])
    os.chdir(project_name)
    print("🎻 Symfony project created with Composer")


def main():
    """Main function."""
    print("=" * 50)
    print("🚀 Create Project - Web project creation script")
    print("=" * 50)

    # Check Node.js
    ensure_node_version()

    # Project name
    project_name = get_project_name()

    # Project type
    project_type = get_project_type()

    # Specific options based on type
    react_type = None
    nextjs_options = None

    if project_type == "2":  # React
        react_type = get_react_type()
    elif project_type == "3":  # Next.js
        nextjs_options = get_nextjs_options()

    # Description and author
    description = get_description()
    author = get_author()

    # License
    license_choice = get_license()

    print("\n⏳ Creating project...")

    # Create project based on type
    if project_type == "1":  # HTML/CSS (empty)
        create_empty_project(project_name)
    elif project_type == "2":  # React
        create_react_project(project_name, react_type)
    elif project_type == "3":  # Next.js
        create_nextjs_project(project_name, nextjs_options)
    elif project_type == "4":  # Astro
        create_astro_project(project_name)
    elif project_type == "5":  # Symfony
        create_symfony_project(project_name)

    # Create configuration files
    create_readme(project_name, description)
    create_gitignore()
    create_eslint_prettier_config()

    # Install ESLint and Prettier
    print("\n⏳ Installing ESLint and Prettier...")
    run_command(["npm", "install", "-D", "eslint", "prettier"])
    print("✓ ESLint and Prettier installed")

    # Create license
    if license_choice and license_choice != "4":
        create_license(license_choice, author)

    print("\n" + "=" * 50)
    print(f"🎉 Project '{project_name}' is ready to code!")
    print("=" * 50)
    print(f"\nTo get started:")
    print(f"  cd {os.getcwd()}")
    print(f"  npm run dev")


if __name__ == "__main__":
    main()
