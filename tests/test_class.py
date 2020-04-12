import unittest
from tests.helper import get_parser
from java_parser.clazz import ClassTransformer
from java_parser.method import MethodTransformer
from java_parser.annotation import AnnotationTransformer
from java_parser.common import CommonTransformer
from java_parser.imports import ImportTransformer
from java_parser.package import PackageTransformer
from java_parser.enum import EnumTransformer
from java_parser.field import FieldTransformer


class CompoundClassTransformer(
    CommonTransformer,
    PackageTransformer,
    ImportTransformer,
    AnnotationTransformer,
    FieldTransformer,
    MethodTransformer,
    EnumTransformer,
    ClassTransformer,
):
    pass


class TestClass(unittest.TestCase):
    def test_class_case1(self):

        text = """
/**
* File comment here.
*/
package com.example.springboot;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

/**
* Class comment here.
*/
@RestController
public class HelloController {

    /**
    * Field comment here.
    */
    @Test
    public final static String VERSION = "0.1.1";

    /*
    * Method comment here.
    */
	@RequestMapping("/")
	public String index() {
		return "Greetings from Spring Boot!";
	}

}
        """
        tree = get_parser("clazz").parse(text)
        print(tree)
        result = CompoundClassTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CLASS",
            "name": "HelloController",
            "fields": [
                {
                    "name": "VERSION",
                    "assign": '"0.1.1"',
                    "operator": "=",
                    "classType": "String",
                    "modifiers": ["public", "final", "static"],
                    "annotations": [
                        {
                            "name": "Test",
                            "lineno": 19,
                            "linenoEnd": 19,
                            "type": "ANNOTATION",
                        }
                    ],
                    "comment": ["/**", "* Field comment here.", "*/"],
                    "type": "FIELD",
                    "lineno": 16,
                    "linenoEnd": 20,
                }
            ],
            "methods": [
                {
                    "name": "index",
                    "body": [
                        {
                            "body": '"Greetings from Spring Boot!"',
                            "type": "RETURN",
                            "lineno": 27,
                            "linenoEnd": 27,
                        }
                    ],
                    "returnType": "String",
                    "type": "METHOD",
                    "modifiers": ["public"],
                    "annotations": [
                        {
                            "name": "RequestMapping",
                            "lineno": 25,
                            "linenoEnd": 25,
                            "type": "ANNOTATION",
                            "args": ['"/"'],
                        }
                    ],
                    "comment": ["/*", "* Method comment here.", "*/"],
                    "lineno": 22,
                    "linenoEnd": 28,
                }
            ],
            "modifiers": ["public"],
            "annotations": [
                {
                    "name": "RestController",
                    "lineno": 13,
                    "linenoEnd": 13,
                    "type": "ANNOTATION",
                }
            ],
            "comment": ["/**", "* Class comment here.", "*/"],
            "lineno": 10,
            "linenoEnd": 30,
            "imports": [
                {
                    "value": "org.springframework.web.bind.annotation.RestController",
                    "type": "IMPORT",
                    "lineno": 7,
                    "linenoEnd": 7,
                },
                {
                    "value": "org.springframework.web.bind.annotation.RequestMapping",
                    "type": "IMPORT",
                    "lineno": 8,
                    "linenoEnd": 8,
                },
            ],
            "package": {
                "value": "com.example.springboot",
                "type": "PACKAGE",
                "lineno": 5,
                "linenoEnd": 5,
            },
            "fileComment": ["/**", "* File comment here.", "*/"],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_class_case2(self):

        text = """
package com.example.springboot;

import java.util.Arrays;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class Application {

	private static final String SOME_CONSTANT = "SOME_CONSTANT";
	private static final int INT_CONSTANT = "123";

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

	@Bean
	public CommandLineRunner commandLineRunner(ApplicationContext ctx) {
		return args -> {

			System.out.println("Let's inspect the beans provided by Spring Boot:");

			String[] beanNames = ctx.getBeanDefinitionNames();
			Arrays.sort(beanNames);
			for (String beanName : beanNames) {
				System.out.println(beanName);
			}

		};
	}

}
        """
        tree = get_parser("clazz").parse(text)
        print(tree)
        result = CompoundClassTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CLASS",
            "name": "Application",
            "fields": [
                {
                    "name": "SOME_CONSTANT",
                    "assign": '"SOME_CONSTANT"',
                    "operator": "=",
                    "classType": "String",
                    "modifiers": ["private", "static", "final"],
                    "type": "FIELD",
                    "lineno": 15,
                    "linenoEnd": 15,
                },
                {
                    "name": "INT_CONSTANT",
                    "assign": '"123"',
                    "operator": "=",
                    "classType": "int",
                    "modifiers": ["private", "static", "final"],
                    "type": "FIELD",
                    "lineno": 16,
                    "linenoEnd": 16,
                },
            ],
            "methods": [
                {
                    "name": "main",
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "SpringApplication.run",
                            "args": ["Application.class", "args"],
                            "lineno": 19,
                            "linenoEnd": 19,
                        }
                    ],
                    "parameters": [
                        {
                            "name": "args",
                            "classType": {"name": "String", "arraySuffix": "[]"},
                            "type": "PARAMETER",
                        }
                    ],
                    "returnType": "void",
                    "type": "METHOD",
                    "modifiers": ["public", "static"],
                    "lineno": 18,
                    "linenoEnd": 20,
                },
                {
                    "name": "commandLineRunner",
                    "body": [
                        {
                            "body": {
                                "parameters": ["args"],
                                "body": [
                                    {
                                        "type": "INVOCATION",
                                        "name": "System.out.println",
                                        "args": [
                                            '"Let\'s inspect the beans provided by Spring Boot:"'
                                        ],
                                        "lineno": 26,
                                        "linenoEnd": 26,
                                    },
                                    {
                                        "type": "STATEMENT",
                                        "name": "beanNames",
                                        "assign": {
                                            "name": "ctx.getBeanDefinitionNames",
                                            "type": "INVOCATION",
                                        },
                                        "operator": "=",
                                        "classType": {
                                            "name": "String",
                                            "arraySuffix": "[]",
                                        },
                                        "lineno": 28,
                                        "linenoEnd": 28,
                                    },
                                    {
                                        "type": "INVOCATION",
                                        "name": "Arrays.sort",
                                        "args": ["beanNames"],
                                        "lineno": 29,
                                        "linenoEnd": 29,
                                    },
                                    {
                                        "test": {
                                            "variable": "beanName",
                                            "classType": "String",
                                            "list": "beanNames",
                                            "type": "FOR_EACH_TEST",
                                        },
                                        "type": "FOR_LOOP",
                                        "lineno": 30,
                                        "linenoEnd": 32,
                                        "body": [
                                            {
                                                "type": "INVOCATION",
                                                "name": "System.out.println",
                                                "args": ["beanName"],
                                                "lineno": 31,
                                                "linenoEnd": 31,
                                            }
                                        ],
                                    },
                                ],
                                "type": "LAMBDA_EXPRESSION",
                                "lineno": 24,
                                "linenoEnd": 34,
                            },
                            "type": "RETURN",
                            "lineno": 24,
                            "linenoEnd": 34,
                        }
                    ],
                    "parameters": [
                        {
                            "name": "ctx",
                            "classType": "ApplicationContext",
                            "type": "PARAMETER",
                        }
                    ],
                    "returnType": "CommandLineRunner",
                    "type": "METHOD",
                    "modifiers": ["public"],
                    "annotations": [
                        {
                            "name": "Bean",
                            "lineno": 22,
                            "linenoEnd": 22,
                            "type": "ANNOTATION",
                        }
                    ],
                    "lineno": 22,
                    "linenoEnd": 35,
                },
            ],
            "modifiers": ["public"],
            "annotations": [
                {
                    "name": "SpringBootApplication",
                    "lineno": 12,
                    "linenoEnd": 12,
                    "type": "ANNOTATION",
                }
            ],
            "lineno": 12,
            "linenoEnd": 37,
            "imports": [
                {
                    "value": "java.util.Arrays",
                    "type": "IMPORT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "value": "org.springframework.boot.CommandLineRunner",
                    "type": "IMPORT",
                    "lineno": 6,
                    "linenoEnd": 6,
                },
                {
                    "value": "org.springframework.boot.SpringApplication",
                    "type": "IMPORT",
                    "lineno": 7,
                    "linenoEnd": 7,
                },
                {
                    "value": "org.springframework.boot.autoconfigure.SpringBootApplication",
                    "type": "IMPORT",
                    "lineno": 8,
                    "linenoEnd": 8,
                },
                {
                    "value": "org.springframework.context.ApplicationContext",
                    "type": "IMPORT",
                    "lineno": 9,
                    "linenoEnd": 9,
                },
                {
                    "value": "org.springframework.context.annotation.Bean",
                    "type": "IMPORT",
                    "lineno": 10,
                    "linenoEnd": 10,
                },
            ],
            "package": {
                "value": "com.example.springboot",
                "type": "PACKAGE",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_class_case3(self):

        text = """
package com.example.springboot;

import java.util.Arrays;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class Application {

    /** Inline comment */
    // private static final String NO_NEED = "SOMETHING NOT NEEDED";

    /** Another comment */
	private static final String SOME_CONSTANT = "SOME_CONSTANT";
	private static final int INT_CONSTANT = "123";

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
}
        """
        tree = get_parser("clazz").parse(text)
        print(tree)
        result = CompoundClassTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CLASS",
            "name": "Application",
            "fields": [
                {
                    "name": "SOME_CONSTANT",
                    "assign": '"SOME_CONSTANT"',
                    "operator": "=",
                    "classType": "String",
                    "modifiers": ["private", "static", "final"],
                    "comment": ["/** Inline comment */", "/** Another comment */"],
                    "type": "FIELD",
                    "lineno": 15,
                    "linenoEnd": 19,
                },
                {
                    "name": "INT_CONSTANT",
                    "assign": '"123"',
                    "operator": "=",
                    "classType": "int",
                    "modifiers": ["private", "static", "final"],
                    "type": "FIELD",
                    "lineno": 20,
                    "linenoEnd": 20,
                },
            ],
            "methods": [
                {
                    "name": "main",
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "SpringApplication.run",
                            "args": ["Application.class", "args"],
                            "lineno": 23,
                            "linenoEnd": 23,
                        }
                    ],
                    "parameters": [
                        {
                            "name": "args",
                            "classType": {"name": "String", "arraySuffix": "[]"},
                            "type": "PARAMETER",
                        }
                    ],
                    "returnType": "void",
                    "type": "METHOD",
                    "modifiers": ["public", "static"],
                    "lineno": 22,
                    "linenoEnd": 24,
                }
            ],
            "modifiers": ["public"],
            "annotations": [
                {
                    "name": "SpringBootApplication",
                    "lineno": 12,
                    "linenoEnd": 12,
                    "type": "ANNOTATION",
                }
            ],
            "lineno": 12,
            "linenoEnd": 25,
            "imports": [
                {
                    "value": "java.util.Arrays",
                    "type": "IMPORT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "value": "org.springframework.boot.CommandLineRunner",
                    "type": "IMPORT",
                    "lineno": 6,
                    "linenoEnd": 6,
                },
                {
                    "value": "org.springframework.boot.SpringApplication",
                    "type": "IMPORT",
                    "lineno": 7,
                    "linenoEnd": 7,
                },
                {
                    "value": "org.springframework.boot.autoconfigure.SpringBootApplication",
                    "type": "IMPORT",
                    "lineno": 8,
                    "linenoEnd": 8,
                },
                {
                    "value": "org.springframework.context.ApplicationContext",
                    "type": "IMPORT",
                    "lineno": 9,
                    "linenoEnd": 9,
                },
                {
                    "value": "org.springframework.context.annotation.Bean",
                    "type": "IMPORT",
                    "lineno": 10,
                    "linenoEnd": 10,
                },
            ],
            "package": {
                "value": "com.example.springboot",
                "type": "PACKAGE",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_class_case4(self):

        text = """
package com.example.springboot;

import java.util.Arrays;

public class TestGeneric<T> {
	public static void main(String[] args) {
		doSomething();
	}
}
        """
        tree = get_parser("clazz").parse(text)
        print(tree)
        result = CompoundClassTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CLASS",
            "name": "TestGeneric",
            "methods": [
                {
                    "name": "main",
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomething",
                            "lineno": 8,
                            "linenoEnd": 8,
                        }
                    ],
                    "parameters": [
                        {
                            "name": "args",
                            "classType": {"name": "String", "arraySuffix": "[]"},
                            "type": "PARAMETER",
                        }
                    ],
                    "returnType": "void",
                    "type": "METHOD",
                    "modifiers": ["public", "static"],
                    "lineno": 7,
                    "linenoEnd": 9,
                }
            ],
            "generic": ["T"],
            "modifiers": ["public"],
            "lineno": 6,
            "linenoEnd": 10,
            "imports": [
                {
                    "value": "java.util.Arrays",
                    "type": "IMPORT",
                    "lineno": 4,
                    "linenoEnd": 4,
                }
            ],
            "package": {
                "value": "com.example.springboot",
                "type": "PACKAGE",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_class_case5(self):

        text = """
package com.example.springboot;

import java.util.Arrays;

public class TestGeneric<T> extends ClassType1, ClassType2 
        implements Interface1, Interface2 throws path.to.Exception1, Expection2 {
	public static void main(String[] args) {
		doSomething();
	}
}
        """
        tree = get_parser("clazz").parse(text)
        print(tree)
        result = CompoundClassTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CLASS",
            "name": "TestGeneric",
            "methods": [
                {
                    "name": "main",
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomething",
                            "lineno": 9,
                            "linenoEnd": 9,
                        }
                    ],
                    "parameters": [
                        {
                            "name": "args",
                            "classType": {"name": "String", "arraySuffix": "[]"},
                            "type": "PARAMETER",
                        }
                    ],
                    "returnType": "void",
                    "type": "METHOD",
                    "modifiers": ["public", "static"],
                    "lineno": 8,
                    "linenoEnd": 10,
                }
            ],
            "throws": ["path.to.Exception1", "Expection2"],
            "interfaces": ["Interface1", "Interface2"],
            "superclasses": ["ClassType1", "ClassType2"],
            "generic": ["T"],
            "modifiers": ["public"],
            "lineno": 6,
            "linenoEnd": 11,
            "imports": [
                {
                    "value": "java.util.Arrays",
                    "type": "IMPORT",
                    "lineno": 4,
                    "linenoEnd": 4,
                }
            ],
            "package": {
                "value": "com.example.springboot",
                "type": "PACKAGE",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_class_case6(self):

        text = """
package com.example.springboot;

import java.util.Arrays;

public class TestGeneric<T> extends ClassType1, ClassType2 
        implements Interface1, Interface2 throws path.to.Exception1, Expection2 {
	public static void main(String[] args) {
		doSomething();
	}

    private class InnerClass {
        private static final int INT_CONSTANT = "123";

        public void mainMethod(int a) {
            doSomething();
        }
    }
}
        """
        tree = get_parser("clazz").parse(text)
        print(tree)
        result = CompoundClassTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CLASS",
            "name": "TestGeneric",
            "methods": [
                {
                    "name": "main",
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomething",
                            "lineno": 9,
                            "linenoEnd": 9,
                        }
                    ],
                    "parameters": [
                        {
                            "name": "args",
                            "classType": {"name": "String", "arraySuffix": "[]"},
                            "type": "PARAMETER",
                        }
                    ],
                    "returnType": "void",
                    "type": "METHOD",
                    "modifiers": ["public", "static"],
                    "lineno": 8,
                    "linenoEnd": 10,
                }
            ],
            "innerClasses": [
                {
                    "type": "CLASS",
                    "name": "InnerClass",
                    "fields": [
                        {
                            "name": "INT_CONSTANT",
                            "assign": '"123"',
                            "operator": "=",
                            "classType": "int",
                            "modifiers": ["private", "static", "final"],
                            "type": "FIELD",
                            "lineno": 13,
                            "linenoEnd": 13,
                        }
                    ],
                    "methods": [
                        {
                            "name": "mainMethod",
                            "body": [
                                {
                                    "type": "INVOCATION",
                                    "name": "doSomething",
                                    "lineno": 16,
                                    "linenoEnd": 16,
                                }
                            ],
                            "parameters": [
                                {"name": "a", "classType": "int", "type": "PARAMETER"}
                            ],
                            "returnType": "void",
                            "type": "METHOD",
                            "modifiers": ["public"],
                            "lineno": 15,
                            "linenoEnd": 17,
                        }
                    ],
                    "modifiers": ["private"],
                    "lineno": 12,
                    "linenoEnd": 18,
                }
            ],
            "throws": ["path.to.Exception1", "Expection2"],
            "interfaces": ["Interface1", "Interface2"],
            "superclasses": ["ClassType1", "ClassType2"],
            "generic": ["T"],
            "modifiers": ["public"],
            "lineno": 6,
            "linenoEnd": 19,
            "imports": [
                {
                    "value": "java.util.Arrays",
                    "type": "IMPORT",
                    "lineno": 4,
                    "linenoEnd": 4,
                }
            ],
            "package": {
                "value": "com.example.springboot",
                "type": "PACKAGE",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")
