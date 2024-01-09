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
    @State var savedConversation: [MessagePair] = []

    var body: some Scene {
        WindowGroup {
            ContentView(newConversation: $newConversation, savedConversation: $savedConversation)
        }
    }
}
