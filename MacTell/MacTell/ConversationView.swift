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

    @State private var userInput = ""


    var body: some View {
        VStack {
            ScrollView {
                ForEach($conversation, id: \.id) {
                    $messagePair in MessageView(messagePair: $messagePair)
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
    }
    
    func sendMessage() {
        if userInput == "" {
            return
        }

        conversation.append(MessagePair(userInput: userInput))
        self.conversation[conversation.count - 1].sendInputTextToLLM()
        
        DispatchQueue.main.async {
            self.userInput = ""
        }
        
        if autoSave {
            self.conversation[conversation.count - 1].addToBookmarks()
        }
    }
}

struct ConversationView_Previews: PreviewProvider {
    struct DummyView: View {
        @State var tmp_conversation: [MessagePair] = []

        var body: some View {
            ConversationView(conversation: $tmp_conversation, autoSave: false)
        }
    }

    static var previews: some View {
        DummyView()
    }
}
