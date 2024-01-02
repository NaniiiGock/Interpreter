//
//  TmpPythonKitTest.swift
//  InterpreterApp
//
//  Created by Yaroslav Korch on 02.01.2024.
//

import Foundation
import PythonKit
import SwiftUI





struct PythonView: View {
    
    let dirPath = "/Users/mrkorch/Desktop"
    
    @State var textFromPython = "Sample text."
    @State var simpleLib: PythonObject?

    func setUpPython() {
        if (simpleLib != nil) {
            return
        }

        let sys = Python.import("sys")
        sys.path.append(dirPath)
        simpleLib = Python.import("simple")
    }

    var body: some View {
        VStack {
            Text(textFromPython)
            Button("Run Python") {
                self.runPython()
            }
            .padding()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
    
    func runPython() {
        self.setUpPython()
        let res = String(Int(simpleLib!.some_func())!)
        self.textFromPython = "Response from Python: " + res
    }
}

    



#Preview {
    PythonView()
}
