lang_dict = {"c":
"""#include <stdio.h>

int main() {
	printf("Hello World\\n");
	return 0;
}""",
"cpp":
"""#include <iostream> // include API

using namespace std;

int main() // the main code portion of a C++ program
{
   cout << "Hello World" << endl;  //print Hello World on the screen
   return 0; // conventional
}""",
"c++":
"""#include <iostream> // include API

using namespace std;

int main() // the main code portion of a C++ program
{
   cout << "Hello World" << endl;  //print Hello World on the screen
   return 0; // conventional
}""",
"java":
"""public class Java {
	public static void main(String[] args) {
		System.out.println("Hello World");
	}
}""",
"python":
"""print "Hello World!" """,
"python3":
"""print("Hello World!")""",
 "bash":
"""#!/bin/bash
echo \"Hello World!\"""",
"javascript":
"""console.log("Hello World");""",
"angular":
"""$scope.$log = $log;
$scope.message = 'Hello World!';""",
"csharp":
"""class HelloWorld {
	static void Main() {
		System.Console.WriteLine("Hello World");
	}
}""",
"c#":
"""class HelloWorld {
	static void Main() {
		System.Console.WriteLine("Hello World");
	}
}""",
"coffeescript":
"""alert \"Hello, World!\"""",
"go":
"""package main

import "fmt"

func main() {
  fmt.Printf("Hello World!\\n")
}""",
"latex":
"""\\documentclass{article}
\\begin{document}
\\Hello World
\\end{document}""",
"nodejs":
"""console.log('Hello world!');""",
"node.js":
"""console.log('Hello world!');""",
 "php":
"""<?php
echo 'Hello World';""",
 "r":
"""cat("Hello world\\n")""",
 "ruby":
"""#!/usr/bin/env ruby
puts \"Hello World\"""",
"sql":
"""CREATE TABLE HELLO (HELLO CHAR(12))
INSERT INTO HELLO VALUES ('HELLO WORLD!')
SELECT * FROM HELLO""",
"swift":
"""print("Hello World")""",
"rust":
"""fn main() {
    println!("Hello, world!");
}""",
"tcl":
"""puts \"Hello World\"""",
"tsql":
"""DECLARE @message varchar(128)
SELECT  @message = 'Hello World!'
PRINT @message""",
"mysql":
"""SELECT 'Hello World!';""",
"perl":
"""#!/usr/local/bin/perl -w
use CGI;                             # load CGI routines
$q = CGI->new;                        # create new CGI object
print $q->header,                    # create the HTTP header
     $q->start_html('hello world'), # start the HTML
     $q->h1('hello world'),         # level 1 header
     $q->end_html;                  # end the HTML
# http://perldoc.perl.org/CGI.html""",
 "d":
"""// Hello World in D
import std.stdio;

void main()
{
	   writefln("Hello World!");
}
""",
"pascal":
"""program HelloWorld(output);
begin
    writeln('Hello World');
    readln
end.""",
"fortran":
"""program helloworld
print *,'Hello World'
end program helloworld""",
"haskell":
"""module Main where

main = putStrLn \"Hello, World!\"""",
"vb":
"""Module HelloWorld
    Sub Main()
        MsgBox("Hello world!")
    End Sub
End Module""",
"visualbasic":
"""Module HelloWorld
    Sub Main()
        MsgBox("Hello world!")
    End Sub
End Module""",
"shell":
"""#!/bin/sh
echo \"Hello World\""""
}
