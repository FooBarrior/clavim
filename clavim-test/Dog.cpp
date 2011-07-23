#include "Dog.hpp"

Dog::Dog(char *aName) {
    name = aName;
}

char *Dog::getName() {
    return name;
}
