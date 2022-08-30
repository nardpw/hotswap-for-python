# Hotswap for Python

# Install

`pip install hotcodeswap`

# Usage

Decorate the main function with @hotswap.main

# Example
```python
import hotswap
from time import sleep

def function():
    print('hoge')

class Calculater:

    def add(self, x, y):
        return x + y

@hotswap.main # add this to main function
def main():   # cannot be hot-swapped to the main function
    calc = Calculater()
    while True:
        function()
        print(calc.add(2, 3))
        sleep(1)

if __name__ == '__main__':
    main()

```
