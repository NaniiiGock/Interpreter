//
//  ConversationView.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI

struct ConversationView: View {
    @Binding var conversation: [MessagePair]
    let autoSave: Bool
    var onDelete: ((MessagePair) -> Void)?

    @State private var userInput = ""

    var body: some View {
        VStack {
            ScrollView {
                ForEach($conversation, id: \.id) {
                    $messagePair in MessageView(messagePair: messagePair, onDelete: self.onDelete)
                }
            }
            // .defaultScrollAnchor(.bottom)

            HStack {
                TextField("Type a message", text: $userInput, onCommit: sendMessage)
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                Button(action: sendMessage) {
                    Image(systemName: "paperplane.fill")
                }
            }
            .padding()
        }
    }

    func sendMessage() {
        if userInput == "" {
            return
        }

        DispatchQueue.main.async {
            conversation.append(MessagePair(userInput: userInput))
            self.userInput = ""
            self.conversation[conversation.count - 1].sendInputTextToLLM()

            if autoSave {
                self.conversation[conversation.count - 1].addToBookmarks()
            }
        }
    }
}
