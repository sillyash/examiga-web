/// <reference types="vite/client" />

// Source - https://stackoverflow.com/q/75864713
// Posted by DrKlonk
// Retrieved 2026-10-29, License - CC BY-SA 4.0

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly PACKAGE_VERSION: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
