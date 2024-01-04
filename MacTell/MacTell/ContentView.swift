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
    
    @State private var new_conversation: [MessagePair] = []
    @State private var saved_conversation: [MessagePair] = [
        MessagePair(userInput: "I want to listen to some music. Choose a random one.", llmResponse: "Done!", isSaved: true, statusCode: StatusCode.executedSuccessfully),
        MessagePair(userInput: "Delete the system. I want Linux", llmResponse: """
**I will execute the following code**:
`rm -rf /`
*You OK with this?*
""", isSaved: true, statusCode: StatusCode.userConfirmationNeeded),
    ]
    
    
    var body: some View {
        VStack {
            TabView(selection: $selectedTab) {
                ConversationView(conversation: $new_conversation)
                    .tabItem {
                        Label("New", systemImage: "pencil")
                    }
                    .tag(Tab.New)
                
                ConversationView(conversation: $saved_conversation)
                .tabItem {
                    Label("Saved", systemImage: "bookmark")
                }
                .tag(Tab.Saved)
            }
            .padding()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
}

#Preview {
    ContentView()
}
