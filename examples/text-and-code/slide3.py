from pyzlides import Head3, BodyText, Code

slide = [
    Head3("Code Component Demo"),
    BodyText("Here's an example of Python code with syntax highlighting:"),
    Code("""
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Generate first 10 Fibonacci numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")""", "python"),
    BodyText("And here's some JavaScript code:"),
    Code("""
function greetUser(name) {
    const greeting = `Hello, ${name}!`;
    console.log(greeting);
    return greeting;
}

// Usage example
const userName = "World";
greetUser(userName);""", "javascript"),
    BodyText("Code blocks automatically handle long lines and maintain proper formatting.")
]