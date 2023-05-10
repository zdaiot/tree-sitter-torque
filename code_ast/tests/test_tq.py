import sys
sys.path.insert(0, './code_ast')
import code_ast
print(code_ast)
from code_ast import ast


def run_code_cst(code_str: str, lang: str="cpp"):
    # Parse the code
    source_ast = ast(code_str, lang=lang, syntax_error='warn')
    return source_ast


if __name__ == '__main__':
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

    visit_result = run_code_cst(code, lang='torque')
    print(visit_result)
