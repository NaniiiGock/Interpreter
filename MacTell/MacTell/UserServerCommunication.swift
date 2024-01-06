//
//  AsyncLearning.swift
//  MacTell
//
//  Created by Yaroslav Korch on 06.01.2024.
//

import Foundation
import PythonKit
import SwiftUI


enum InteractionType: Int, Codable {
    case Default = -1
    // user requests
    case SendingInput = 0
    case SendingConfirmation = 1
    case AskingRerun = 2
    case SaveToBookmarks = 3
    case RemoveFromBookmarks = 4
    case DeleteAllUnsavedFromDB = 5
    case DeleteUserMessage = 6

    // server responses
    case ReturningLLMResponse = 7
    case ReturningCommandsResults = 8
}

struct UserServerInteractionData: Codable {
    var type: InteractionType = InteractionType.Default

    var uuid: String = ""
    var userInput: String = ""
    var llmResponse: String = ""
    var StdOut: String = ""
    var StdErr: String = ""
    var Date: String = ""
    var statusCode: StatusCode = StatusCode.noActionTaken
}



class UserServerInteractionDataBuilder {
    public var userServerInteractionData: UserServerInteractionData = UserServerInteractionData()
    
    
    func addUUID(messagePair: MessagePair) {
        self.userServerInteractionData.uuid = messagePair.id.uuidString
    }
    
    func addDate(messagePair: MessagePair) {
        self.userServerInteractionData.Date = messagePair.formattedDate
    }
    
    func build_all(messagePair: MessagePair) -> UserServerInteractionData {
        self.addUUID(messagePair: messagePair)
        self.addDate(messagePair: messagePair)
        return self.userServerInteractionData
    }
}
