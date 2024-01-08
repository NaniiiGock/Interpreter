//
//  AsyncLearning.swift
//  MacTell
//
//  Created by Yaroslav Korch on 06.01.2024.
//

import Foundation
import PythonKit
import SwiftUI

struct UserServerInteractionData: Codable {
    var statusCode: StatusCode = .noActionTaken

    var UUID: String = ""
    var userInput: String = ""
    var llmResponse: String = ""
    var StdOut: String = ""
    var StdErr: String = ""
    var Date: String = ""
}

class UserServerInteractionDataBuilder {
    public var userServerInteractionData: UserServerInteractionData?

    func refresh() -> UserServerInteractionDataBuilder {
        self.userServerInteractionData = UserServerInteractionData()
        return self
    }

    func addUUID(messagePair: MessagePair) -> UserServerInteractionDataBuilder {
        self.userServerInteractionData?.UUID = messagePair.id.uuidString
        return self
    }

    func addUserInput(messagePair: MessagePair) -> UserServerInteractionDataBuilder {
        self.userServerInteractionData?.userInput = messagePair.userInput
        return self
    }

    func addDate(messagePair: MessagePair) {
        self.userServerInteractionData?.Date = messagePair.date
    }

    func build_all(messagePair: MessagePair) -> UserServerInteractionData {
        self.refresh()
            .addUUID(messagePair: messagePair)
            .addUserInput(messagePair: messagePair)
            .addDate(messagePair: messagePair)

        return self.userServerInteractionData!
    }
}
