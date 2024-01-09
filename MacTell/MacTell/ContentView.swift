//
//  ContentView.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI

enum Tab {
    case New, Saved
}

struct ContentView: View {
    @State private var selectedTab: Tab = .New

    @Binding public var newConversation: [MessagePair]
    @Binding public var savedConversation: [MessagePair]

    var body: some View {
        VStack {
            TabView(selection: $selectedTab) {
                ConversationView(conversation: $newConversation, autoSave: false, onDelete: self.onDelete)
                    .tabItem {
                        Label("New", systemImage: "pencil")
                    }
                    .tag(Tab.New)

                ConversationView(conversation: $savedConversation, autoSave: true, onDelete: self.onDelete)
                    .tabItem {
                        Label("Saved", systemImage: "bookmark")
                    }
                    .tag(Tab.Saved)
            }
            .padding()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .onChange(of: selectedTab) { oldTab in
                tabChanged(to: oldTab)
            }
        }
        .onAppear {
            WebSocketManager.shared.onMessageReceived = self.redirectReceivedData
            WebSocketManager.shared.onPlethoraMessagesReceived = self.replaceSavedMessages

            WebSocketManager.shared.connect()
            WebSocketManager.shared.sendMessage(UserServerInteractionData(statusCode: .askAllSaved))
        }
    }

    private func tabChanged(to _: Tab) {
        // here `selectedTab` is already modified.
        if selectedTab == Tab.New {
            filterUnsavedMessages()
        }
        else if selectedTab == Tab.Saved {
            verifySavedMessages()
        }
    }

    private func filterUnsavedMessages() {
        savedConversation = savedConversation.filter { $0.isSaved }
    }

    private func verifySavedMessages() {
        filterUnsavedMessages()

        let newSaved = newConversation.filter { $0.isSaved }
        for item in newSaved {
            if !savedConversation.contains(where: { $0.id == item.id }) {
                savedConversation.append(item)
            }
        }
    }

    private func redirectReceivedData(userServerInteractionData: UserServerInteractionData) {
        guard let receivedUUID = UUID(uuidString: userServerInteractionData.UUID) else {
            fatalError("Invalid UUID string")
        }

        var messagePairInInterest: MessagePair?

        if let index = newConversation.firstIndex(where: { $0.id == receivedUUID }) {
            messagePairInInterest = newConversation[index]
        }
        if let index = savedConversation.firstIndex(where: { $0.id == receivedUUID }) {
            messagePairInInterest = savedConversation[index]
        }

        if messagePairInInterest == nil {
            print("WARNING: MessagePair not found for received UUID")
            return
        }
        messagePairInInterest!.processReceivedData(userServerInteractionData: userServerInteractionData)
    }

    private func replaceSavedMessages(USIDArr: [UserServerInteractionData]) {
        savedConversation = USIDArr.map { USID in
            MessagePair(id: UUID(uuidString: USID.UUID)!, userInput: USID.userInput, llmResponse: LocalizedStringKey(USID.llmResponse), isSaved: true, statusCode: USID.statusCode, date: USID.Date, stdOut: USID.StdOut, stdErr: USID.StdErr)
        }
    }
    
    private func onDelete(messagePair: MessagePair) {
        DispatchQueue.main.async {
            let toDeleteUUID = messagePair.id

            var sendDeleteMessage = false

            if let index = newConversation.firstIndex(where: { $0.id == toDeleteUUID }) {
                newConversation.remove(at: index)
                sendDeleteMessage = true
            }

            if let index = savedConversation.firstIndex(where: { $0.id == toDeleteUUID }) {
                savedConversation.remove(at: index)
                sendDeleteMessage = true
            }

            if sendDeleteMessage {
                WebSocketManager.shared.sendMessage(UserServerInteractionData(statusCode: .deleteUserMessage, UUID: toDeleteUUID.uuidString))
            }
            
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    struct PreviewWrapper: View {
        @State var newConversation: [MessagePair] = []
        @State var savedConversation: [MessagePair] = [
            MessagePair(userInput: "I want to listen to some music. Choose a random one.", llmResponse: "Done!", isSaved: true, statusCode: StatusCode.executedSuccessfully),
            MessagePair(userInput: "Delete the system. I want Linux", llmResponse: """
            **I will execute the following code**:
            `rm -rf /`
            *You OK with this?*
            """, isSaved: true, statusCode: StatusCode.askConfirmation)
        ]

        var body: some View {
            ContentView(newConversation: $newConversation, savedConversation: $savedConversation)
        }
    }

    static var previews: some View {
        PreviewWrapper()
    }
}
