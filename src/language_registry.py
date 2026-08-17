import os
import re
import json

class LanguageManifestParser:
    """Base class for language-specific manifest parsers."""
    
    def get_patterns(self) -> list:
        """Return a list of glob patterns for manifest files (e.g., ['**/pom.xml'])."""
        return []

    def is_manifest(self, file_path: str) -> bool:
        """Return True if this specific file path is considered a manifest to parse."""
        return False

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        """Parse the manifest content and add findings to the dependencies and frameworks sets."""
        pass


class CSharpParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/*.csproj", "**/global.json", "**/appsettings*.json", "**/Program.cs", "**/Startup.cs"]

    def is_manifest(self, file_path: str) -> bool:
        return file_path.endswith(".csproj")

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        if file_path.endswith(".csproj"):
            # Supports both <TargetFramework> and <TargetFrameworks> (multi-targeting)
            tf_matches = re.findall(r'<TargetFrameworks?>(.*?)</TargetFrameworks?>', content)
            for tf in tf_matches:
                for target in tf.split(';'):
                    if target.strip():
                        frameworks.add(target.strip())
            
            # Supports flexible attribute quotes (Include="..." or Include='...')
            pkg_matches = re.findall(r'<PackageReference\s+[^>]*Include=["\']([^"\']+)["\']', content)
            for pkg in pkg_matches:
                dependencies.add(pkg)


class JavaParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/pom.xml", "**/build.gradle", "**/build.gradle.kts", "**/application.properties", "**/application.yml"]

    def is_manifest(self, file_path: str) -> bool:
        filename = os.path.basename(file_path)
        return filename in ["pom.xml", "build.gradle", "build.gradle.kts"]

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        filename = os.path.basename(file_path)
        if filename == "pom.xml":
            dep_matches = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
            for dep in dep_matches:
                dependencies.add(dep)
        elif "build.gradle" in filename:
            dep_matches = re.findall(r'(?:implementation|api|compile|runtimeOnly)\s+[\'"]([^\'"]+)[\'"]', content)
            for dep in dep_matches:
                dependencies.add(dep)


class NodeParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/package.json", "**/tsconfig.json"]

    def is_manifest(self, file_path: str) -> bool:
        return os.path.basename(file_path) == "package.json"

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        if os.path.basename(file_path) == "package.json":
            try:
                pkg_data = json.loads(content)
                for key in ['dependencies', 'devDependencies', 'peerDependencies']:
                    if key in pkg_data and isinstance(pkg_data[key], dict):
                        dependencies.update(pkg_data[key].keys())
            except Exception:
                pass


class PythonParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/requirements.txt", "**/pyproject.toml", "**/Pipfile", "**/setup.py"]

    def is_manifest(self, file_path: str) -> bool:
        filename = os.path.basename(file_path)
        return filename in ["requirements.txt", "pyproject.toml", "Pipfile"]

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        filename = os.path.basename(file_path)
        if filename == "requirements.txt":
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-"):
                    pkg_name = re.split(r'[=<>;~]', line)[0].strip()
                    if pkg_name:
                        dependencies.add(pkg_name)
        elif filename == "pyproject.toml":
            # Extracts dependency keys from standard pyproject.toml / poetry sections
            for line in content.splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#") and not line.startswith("["):
                    key = line.split("=")[0].strip()
                    if key and not key.startswith("python"):
                        dependencies.add(key)


class DockerParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/docker-compose.yml", "**/docker-compose.yaml", "**/Dockerfile"]

    def is_manifest(self, file_path: str) -> bool:
        filename = os.path.basename(file_path)
        return filename in ["docker-compose.yml", "docker-compose.yaml", "Dockerfile"]

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        filename = os.path.basename(file_path)
        if "Dockerfile" in filename:
            from_matches = re.findall(r'^FROM\s+([^\s]+)', content, re.MULTILINE | re.IGNORECASE)
            for img in from_matches:
                frameworks.add(f"docker:{img}")
        elif "docker-compose" in filename:
            image_matches = re.findall(r'image:\s*([^\s]+)', content)
            for img in image_matches:
                frameworks.add(f"docker:{img}")


# Register all parsers
PARSERS = [
    CSharpParser(),
    JavaParser(),
    NodeParser(),
    PythonParser(),
    DockerParser()
]
