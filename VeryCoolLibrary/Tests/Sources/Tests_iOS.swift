//
//  Tests_iOS.swift
//  Tests iOS
//
//  Created by Narlei Américo Moreira on 14/04/21.
//

import XCTest
import VeryCoolLibrary

class Tests_iOS: XCTestCase {
    func testExample() throws {
        XCTAssert(VeryCoolLibrary.coolText() == "Text")
    }
}
