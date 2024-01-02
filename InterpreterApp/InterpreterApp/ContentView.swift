//
//  ContentView.swift
//  InterpreterApp
//
//  Created by Yaroslav Korch on 02.01.2024.
//

import SwiftUI


struct ContentView: View {
    @State private var userInput = ""
    @State private var messageHistory: [String] = []
    @State private var scrollToBottom = false

    var body: some View {
        VStack {
            ScrollViewReader { proxy in
                List(messageHistory, id: \.self) { message in
                    if message.contains("Interpreter:") {
                        Text(message)
                            .foregroundColor(.purple)
                    } else {
                        Text(message)
                    }
                }
                .padding()
                .onChange(of: messageHistory) { _ in
                    scrollToBottom = true
                    withAnimation {
                        proxy.scrollTo(messageHistory.last ?? "", anchor: .bottom)
                    }
                }
            }

            HStack {
                TextField("Type a message", text: $userInput, onCommit: sendMessage)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                Button("Send") {
                    sendMessage()
                }
                .padding()
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    func sendMessage() {
        if !userInput.isEmpty {
            messageHistory.append("User: \(userInput)")
            messageHistory.append("Interpreter: you said \(userInput)")
            userInput = ""
        }
    }
}


#Preview {
    ContentView()
}
