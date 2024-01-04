//
//  ContentView.swift
//  InterpreterApp
//
//  Created by Yaroslav Korch on 02.01.2024.
//

import SwiftUI



struct ChatMessage {
    let text: String
    let isFromUser: Bool
    var toSave: Bool = false
}

struct ContentView: View {
    @State private var userInput = ""
    @State private var messageHistory: [ChatMessage] = []
    @State private var selectedTab = "Blank"

    var body: some View {
        TabView(selection: $selectedTab) {
            chatView
                .tabItem {
                    Label("Blank", systemImage: "bubble.left")
                }
                .tag("Blank")

            Text("Saved Chats will be shown here")
                .tabItem {
                    Label("Saved", systemImage: "bookmark")
                }
                .tag("Saved")
        }
        .toolbar {
            ToolbarItem(placement: .navigation) {
                Button(action: {}) {
                    Image(systemName: "line.horizontal.3")
                }
            }
        }
    }

    var chatView: some View {
        VStack {
            ScrollView {
                ForEach(messageHistory, id: \.text) { message in
                    MessageView(message: message)
                }
            }

            HStack {
                TextField("Type a message", text: $userInput, onCommit: sendMessage)
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                Button(action: sendMessage) {
                    Image(systemName: "paperplane.fill")
                }
            }
            .padding()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    func sendMessage() {
        if !userInput.isEmpty {
            let userMessage = ChatMessage(text: "User: \(userInput)", isFromUser: true)
            let interpreterMessage = ChatMessage(text: "Interpreter: you said \(userInput)", isFromUser: false)

            messageHistory.append(userMessage)
            messageHistory.append(interpreterMessage)
            userInput = ""
        }
    }
}

struct MessageView: View {
    var message: ChatMessage

    var body: some View {
        HStack {
            if message.isFromUser {
                Spacer()
            }

            VStack(alignment: message.isFromUser ? .trailing : .leading) {
                Text(message.text)
                    .padding()
                    .background(message.isFromUser ? Color.blue : Color.gray)
                    .cornerRadius(15)
                    .foregroundColor(.white)

                if !message.isFromUser {
                    HStack {
                        Button(action: {}) {
                            Image(systemName: "bookmark")
                        }

                        Button(action: {}) {
                            Image(systemName: "arrow.triangle.2.circlepath")
                        }
                    }
                }
            }

            if !message.isFromUser {
                Spacer()
            }
        }
        .padding(message.isFromUser ? .trailing : .leading)
    }
}


#Preview {
    ContentView()
}
