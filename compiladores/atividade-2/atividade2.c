// C program to illustrate the regexec() function
#include <regex.h>
#include <stdio.h>

// Function to print the result
void print_result(int value)
{

	// If pattern found
	if (value == 0) {
		printf("Pattern found.\n");
	}

	// If pattern not found
	else if (value == REG_NOMATCH) {
		printf("Pattern not found.\n");
	}

	// If error occurred during Pattern
	// matching
	else {
		printf("An error occurred.\n");
	}
}

// Driver Code
int main()
{

	// Variable to store initial regex()
	regex_t reegex;

	// Variable for return type
	int value;
	int value2;

	// Creation of regEx
	value = regcomp( &reegex, "Welcome to GfG", 0);

	// Comparing pattern "GeeksforGeeks" with
	// string in reg
	value = regexec( &reegex, "GeeksforGeeks",
					0, NULL, 0);

	// Creation of regEx
	value2 = regcomp( &reegex, "GeeksforGeeks", 0);

	// Comparing pattern "Geeks"
	// with string in reg
	value2 = regexec( &reegex, "GeeksforGeeks",
					0, NULL, 0);

	// Print the results
	print_result(value);
	print_result(value2);
	return 0;
}
