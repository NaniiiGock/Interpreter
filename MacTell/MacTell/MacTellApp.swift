//
//  MacTellApp.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI

@main
struct MacTellApp: App {
    @State var newConversation: [MessagePair] = []
    @State var savedConversation: [MessagePair] = [
//        MessagePair(userInput: "I want to listen to some music. Choose a random one.", llmResponse: "Done!", isSaved: true, statusCode: StatusCode.executedSuccessfully),
//        MessagePair(userInput: "Delete the system. I want Linux", llmResponse: """
//        **I will execute the following code**:
//        `rm -rf /`
//        *You OK with this?*
//        """, isSaved: true, statusCode: StatusCode.askConfirmation)
    ]

    var body: some Scene {
        WindowGroup {
            ContentView(newConversation: $newConversation, savedConversation: $savedConversation)
        }
    }
}
