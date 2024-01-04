//
//  ConversationView.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI


struct ConversationView: View {
    @Binding var conversation: [MessagePair]
    public let autoSave = false

    @State private var userInput = ""
    
    // @State public var PythonLibManager


    var body: some View {
        VStack {
            ScrollView {
                ForEach($conversation, id: \.id) {
                    $messagePair in MessageView(messagePair: $messagePair,
                                                onBookmark: { toggleBookmarkMessagePair(for: messagePair) }
)
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
        sendInputTextToLLM()
    
        DispatchQueue.main.async {
            self.userInput = ""
        }
        
        if autoSave {
            toggleBookmarkMessagePair(for: self.conversation[conversation.count - 1])
        }
    }
    
    
    func sendMessageToLLM(messagePair: MessagePair) -> (String, StatusCode) {
        // TODO: integrate Python
        return ("LLM Response: *huh?*", StatusCode.sentForExecution)
    }

    func sendInputTextToLLM() {
        guard !conversation.isEmpty else { fatalError("Empty `conversation`!") }
        

        let last_ind = self.conversation.count - 1
        let last_message_pair = self.conversation[last_ind]
        
        let (llmResponse, responseCode) = sendMessageToLLM(messagePair: last_message_pair)
    
        self.conversation[last_ind].receiveLLMResponse(llmResponse: LocalizedStringKey(llmResponse), statusCode: responseCode)
        }
    
    func toggleBookmarkMessagePair(for messagePair: MessagePair) {
        // TODO: integrate Python
        let index = conversation.firstIndex(where: { $0.id == messagePair.id })
        
        if index! < 0 {
            fatalError("Something went wrong")
        }
        
        conversation[index!].toggle_bookmark()
    }
}

struct ConversationView_Previews: PreviewProvider {
    struct DummyView: View {
        @State var tmp_conversation: [MessagePair] = []

        var body: some View {
            ConversationView(conversation: $tmp_conversation)
        }
    }

    static var previews: some View {
        DummyView()
    }
}
