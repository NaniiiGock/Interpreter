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
    @State private var selectedTab: Tab = Tab.New
    
    @State private var newConversation: [MessagePair] = []
    // TODO: fetch from the DB
    @State private var savedConversation: [MessagePair] = [
        MessagePair(userInput: "I want to listen to some music. Choose a random one.", llmResponse: "Done!", isSaved: true, statusCode: StatusCode.executedSuccessfully),
        MessagePair(userInput: "Delete the system. I want Linux", llmResponse: """
**I will execute the following code**:
`rm -rf /`
*You OK with this?*
""", isSaved: true, statusCode: StatusCode.askConfirmation),
    ]
    
    
    var body: some View {
        VStack {
            TabView(selection: $selectedTab) {
                
                ConversationView(conversation: $newConversation, autoSave: false)
                    .tabItem {
                        Label("New", systemImage: "pencil")
                    }
                    .tag(Tab.New)
                
                ConversationView(conversation: $savedConversation, autoSave: true)
                    .tabItem {
                        Label("Saved", systemImage: "bookmark")
                    }
                    .tag(Tab.Saved)
            }
            .padding()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .onChange(of: selectedTab) { oldTab, _ in
                tabChanged(to: oldTab)
            }
        }
    }
    
    private func tabChanged(to oldTab: Tab) {
        if oldTab == Tab.Saved {
            filterUnsavedMessages()
        }
        else if oldTab == Tab.New {
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
}

#Preview {
    ContentView()
}
