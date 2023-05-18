tree-sitter-typescript
===========================

[![Build Status](https://github.com/tree-sitter/tree-sitter-typescript/workflows/build/badge.svg)](https://github.com/tree-sitter/tree-sitter-typescript/actions?query=workflow%3Abuild)
[![Build status](https://ci.appveyor.com/api/projects/status/rn11gs5y3tm7tuy0/branch/master?svg=true)](https://ci.appveyor.com/project/maxbrunsfeld/tree-sitter-typescript/branch/master)

TypeScript and TSX grammars for [tree-sitter][].

Because TSX and TypeScript are actually two different dialects, this module defines two grammars. Require them as follows:

```js
require('tree-sitter-typescript').typescript; // TypeScript grammar
require('tree-sitter-typescript').tsx; // TSX grammar
```

For Javascript files with [flow] type annotations you can use the the `tsx` parser.

[tree-sitter]: https://github.com/tree-sitter/tree-sitter
[flow]: https://flow.org/en/

References

* [TypeScript Language Spec](https://github.com/microsoft/TypeScript/blob/main/doc/spec-ARCHIVED.md)


## 开始

### centos下

```bash
yum install nodejs
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
cargo install tree-sitter-cli
```

然后去掉`package.json`中关于`tree-sitter-cli`的安装。

```bash
npm install
npm run build
npm run test
npm run test-load
```

### Linux下安装（舍弃，tree-sitter 提示 glibc版本过低）

若报错`error lto1: fatal error: bytecode stream in file ‘Release/obj.target/tree_sitter_javascript_binding/src/parser.o’ generated with LTO version 2.2 instead of the expected 7.3`，则将`binding.gyp`中的编译指令更改如下：

```
# 添加"-fno-lto"
      "cflags_c": [
        "-std=c99",
        "-fno-lto",
      ]
```

> 可能`tree-sitter-typescript`以及`tree-sitter-javascript`都需要对应的更改。

### windows下安装（舍弃，npm run奇怪错误）

先安装vs2022，并确保选上了`Desktop development with C++`。

然后设置如下：

```
npm config set msvs_version 2022
```

> 若Python也需要设置，可以使用`npm config set python python3.10`.

然后遇到报错`VCINSTALLDIR not set, not running in VS Command Prompt`, 可以参考 https://github.com/nodejs/node-gyp/blob/main/docs/Updating-npm-bundled-node-gyp.md#windows

## tree-sitter学习

1. 有关[precedences](https://github.com/tree-sitter/tree-sitter/pull/939)

2. 有关dynamic precedence

- [dynamic precedence](https://github.com/tree-sitter/tree-sitter/issues/678)

- [dynamic precedence pr](https://github.com/tree-sitter/tree-sitter/pull/87)

- [Corner cases with GLR, precedence, and non-associativity: Intended Semantics?](https://stackoverflow.com/questions/56982408/corner-cases-with-glr-precedence-and-non-associativity-intended-semantics)
