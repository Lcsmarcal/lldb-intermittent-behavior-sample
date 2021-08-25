protocol SomeViewProtocol {
    func doSomething()
}

final class SomeView: SomeViewProtocol {
    func doSomething() {
        print("something done")
    }
}
