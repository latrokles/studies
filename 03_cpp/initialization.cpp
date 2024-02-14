#include <iostream>


/* compile this with:
 * c++ -std=c++0x
 */
int main() {
	char mychar{ 'a' };
	int myint{ 123 };
	double mydouble{ 456.78 };

	std::cout << "The value of mychar is " << mychar << '\n';
	std::cout << "The value of myint is " << myint << '\n';
	std::cout << "The value of mydouble is " << mydouble << '\n';
}
