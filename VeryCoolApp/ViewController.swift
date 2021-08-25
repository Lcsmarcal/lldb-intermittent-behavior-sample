import UIKit

final class ViewController: UIViewController {
    let someView: SomeViewProtocol = SomeView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("Breakpoint here")
    }
}
