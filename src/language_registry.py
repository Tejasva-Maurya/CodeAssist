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
            tf_match = re.search(r'<TargetFramework>(.*?)</TargetFramework>', content)
            if tf_match:
                frameworks.add(tf_match.group(1))
            pkg_matches = re.findall(r'<PackageReference\s+Include="([^"]+)"', content)
            for pkg in pkg_matches:
                dependencies.add(pkg)


class JavaParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/pom.xml", "**/build.gradle", "**/application.properties", "**/application.yml"]

    def is_manifest(self, file_path: str) -> bool:
        return file_path.endswith("pom.xml")

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        if file_path.endswith("pom.xml"):
            dep_matches = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
            for dep in dep_matches:
                dependencies.add(dep)


class NodeParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/package.json", "**/tsconfig.json"]

    def is_manifest(self, file_path: str) -> bool:
        return file_path.endswith("package.json")

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        if file_path.endswith("package.json"):
            try:
                pkg_data = json.loads(content)
                if 'dependencies' in pkg_data:
                    dependencies.update(pkg_data['dependencies'].keys())
            except Exception:
                pass


class PythonParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/requirements.txt", "**/pyproject.toml"]

    def is_manifest(self, file_path: str) -> bool:
        return False # No deep parsing implemented yet, just discovery

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        pass


class DockerParser(LanguageManifestParser):
    def get_patterns(self) -> list:
        return ["**/docker-compose.yml", "**/docker-compose.yaml"]

    def is_manifest(self, file_path: str) -> bool:
        return False

    def parse(self, file_path: str, content: str, dependencies: set, frameworks: set):
        pass


# Register all parsers
PARSERS = [
    CSharpParser(),
    JavaParser(),
    NodeParser(),
    PythonParser(),
    DockerParser()
]
