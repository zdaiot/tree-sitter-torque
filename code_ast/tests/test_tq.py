import sys
sys.path.insert(0, './code_ast')
import code_ast
print(code_ast)
import argparse
from code_ast import ast, match_span
from code_ast import ASTVisitor


def get_length_cum(code_str):
    codes = code_str.split('\n')
    lines_length = [len(x)+1 for idx, x in enumerate(codes) if idx<len(codes)-1]
    cum = 0
    lines_length_cum = []
    for line_length in lines_length:
        cum += line_length
        lines_length_cum.append(cum)
    return lines_length_cum


def convert_xy_x(xy: tuple, lines_length_cum: list):
    x, y = xy
    if x == 0:
        new_x = y
    else:
        new_x = lines_length_cum[x-1] + y
    return new_x


def print_part_code(xy_xy_str, code_str):
    lines_length_cum = get_length_cum(code_str)
    xy_xy = xy_xy_str.split('-')
    xy1 = eval(xy_xy[0])
    x1 = convert_xy_x(xy1, lines_length_cum)
    xy2 = eval(xy_xy[1])
    x2 = convert_xy_x(xy2, lines_length_cum)
    print(code_str[x1: x2+1])


class CustomASTVisitor(ASTVisitor):
    def __init__(self, code_str):
        self._code_str = code_str
        self._code_str_split = code_str.splitlines()
        self._lines_length_cum = get_length_cum(self._code_str)

    def get_part_code(self, start_point, end_point, print_flag=True):
        xs = convert_xy_x(start_point, self._lines_length_cum)
        xe = convert_xy_x(end_point, self._lines_length_cum)
        part_code = self._code_str[xs: xe+1]
        if print_flag:
            print(str(start_point)+', '+str(end_point))
            print(part_code)
        return part_code

    def get_node_info(self, node, print_flag=True):
        xs = convert_xy_x(node.start_point, self._lines_length_cum)
        xe = convert_xy_x(node.end_point, self._lines_length_cum)
        part_code = self._code_str[xs: xe]
        # part_code = match_span(node, self._code_str_split)
        if print_flag:
            print(node)
            print(part_code)
        return part_code

    def visit(self, node):
        self.get_node_info(node)
        print()


def run_code_cst(code_str: str, lang: str="cpp", rebuild: bool=True, 
                 base_repo_url='https://github.com/tree-sitter'):
    # Parse the code
    if lang == 'torque':
        base_repo_url = 'https://github.com/zdaiot'
    source_ast = ast(code_str, lang=lang, rebuild=rebuild, base_repo_url=base_repo_url, syntax_error='warn')
    count_visitor = CustomASTVisitor(code_str)
    source_ast.visit(count_visitor)
    return source_ast


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hunyuan')
    parser.add_argument('--rebuild', default=True, action='store_false')
    args = parser.parse_args()

    code = '''
    transitioning macro TypedArraySpeciesCreateByLength(implicit context: Context)(
        methodName: constexpr string, exemplar: JSTypedArray, length: uintptr):
        JSTypedArray {
    const numArgs: constexpr int31 = 1;
    // TODO(v8:4153): pass length further as uintptr.
    const typedArray: JSTypedArray = TypedArraySpeciesCreate(
        methodName, numArgs, exemplar, Convert<Number>(length), Undefined,
        Undefined);
    try {
        const createdArrayLength =
            LoadJSTypedArrayLengthAndCheckDetached(typedArray)
            otherwise DetachedOrOutOfBounds;
        if (createdArrayLength < length) deferred {
            ThrowTypeError(MessageTemplate::kTypedArrayTooShort);
        }
    } label DetachedOrOutOfBounds {
        ThrowTypeError(MessageTemplate::kTypedArrayTooShort);
    }
    return typedArray;
    }
    '''

    # code = '''
    # @export
    # macro PrintHelloWorld(): void {
    #     Print('Hello world!');
    # }
    # '''

    code = '''
    namespace string {
    // …
    macro TestVisibility() {
        IsJsObject(o); // OK, global namespace visible here
        IsJSArray(o);  // ERROR, not visible in this namespace
        array::IsJSArray(o);  // OK, explicit namespace qualification
    }
    // …
    };
    '''

    # code = '''
    # extern class JSProxy extends JSReceiver {
    #     target: JSReceiver|Null;
    #     handler: JSReceiver|Null;
    # }
    # '''

    # code = '''
    # @export
    # struct PromiseResolvingFunctions {
    #     resolve: JSFunction;
    #     reject: JSFunction;
    # }

    # struct ConstantIterator<T: type> {
    #     macro Empty(): bool {
    #         return false;
    #     }
    #     macro Next(): T labels _NoMore {
    #         return this.value;
    #     }

    #     value: T;
    # }
    # '''

    # code = '''
    # let k: Number = 0;
    # try {
    #     return FastArrayForEach(o, len, callbackfn, thisArg)
    #         otherwise Bailout;
    # }
    # label Bailout(kValue: Smi) deferred {
    #     k = kValue;
    # }
    # '''

    code = '''
    type int32 generates 'TNode<Int32T>' constexpr 'int32_t';
    type int31 extends int32 generates 'TNode<Int32T>' constexpr 'int31_t';
    type Number = Smi | HeapNumber;
    '''

    code = '''
    extern class CoverageInfo extends HeapObject {
        const slot_count: int32;
        slots[slot_count]: CoverageInfoSlot;
    }
    '''

    code = '''
    struct DescriptorEntry {
        key: Name|Undefined;
        details: Smi|Undefined;
        value: JSAny|Weak<Map>|AccessorInfo|AccessorPair|ClassPositions;
    }

    extern class DescriptorArray extends HeapObject {
        const number_of_all_descriptors: uint16;
        number_of_descriptors: uint16;
        raw_number_of_marked_descriptors: uint16;
        filler16_bits: uint16;
        enum_cache: EnumCache;
        descriptors[number_of_all_descriptors]: DescriptorEntry;
    }
    '''

    code = '''
    bitfield struct DebuggerHints extends uint31 {
        side_effect_state: int32: 2 bit;
        debug_is_blackboxed: bool: 1 bit;
        computed_debug_is_blackboxed: bool: 1 bit;
        debugging_id: int32: 20 bit;
    }

    type CompareBuiltinFn = builtin(implicit context: Context)(Object, Object, Object) => Number;
    '''

    code = '''
    extern enum LanguageMode extends Smi {
        kStrict,
        kSloppy
    }
    '''

    code = '''
    typeswitch(language_mode) {
        case (LanguageMode::kStrict): {
            // ...
        }
        case (LanguageMode::kSloppy): {
            // ...
        }
    }
    '''

    code = '''
    intrinsic %RawConstexprCast<To: type, From: type>(f: From): To;
    '''

    visit_result = run_code_cst(code, lang='torque', rebuild=args.rebuild)
    print(visit_result)
