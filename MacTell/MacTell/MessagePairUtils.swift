//
//  MessagePairUtils.swift
//  MacTell
//
//  Created by Yaroslav Korch on 09.01.2024.
//

import Foundation
import SwiftUI


enum StatusCode: Int, Codable {
    case noActionTaken = -1 // default

    case sentForExecution = 0 // command's execution has started.
    case askConfirmation = 1 // app has to ask user for execution confirmation.

    case requestSentToAPI = 2 // app’s UserRequest has been submitted to LLM.

    case submitUserResponse = 3 // The app asks server to submit userInput to LLM.
    case askRerun = 4 // User wants to rerun the command.
    
    case rawText = 5 // LLM Response is a raw text.

    case serverCrash = 7 // CriticalError
    case executedSuccessfully = 10 // The execution was successful
    case executionError = 11 // The execution was unsuccessful

    case saveToBookmarks = 15
    case removeFromBookmarks = 16

    case deleteUserMessage = 18

    case askAllSaved = 19
    case sendAllSaved = 20
}

func getFormattedDate(date: Date) -> String {
    let formatter = DateFormatter()
    formatter.dateStyle = .short
    formatter.timeStyle = .short
    return formatter.string(from: date)
}

struct StatusAppearance {
    var icon: Image
    var text: String
    var color: Color
}

extension MessagePair {
    func getStatusAppearance() -> StatusAppearance {
        // TODO: change the texts
        let appearance: [StatusCode: StatusAppearance] = [
            .noActionTaken: .init(icon: Image(systemName: "ellipsis.circle"), text: "No Action Taken", color: .gray),
            .sentForExecution: .init(icon: Image(systemName: "hourglass"), text: "Sent for Execution", color: .blue),
            .askConfirmation: .init(icon: Image(systemName: "questionmark.circle"), text: "Confirmation Needed", color: .orange),
            .requestSentToAPI: .init(icon: Image(systemName: "paperplane"), text: "Request Sent", color: .green),
            .submitUserResponse: .init(icon: Image(systemName: "text.bubble"), text: "Input Submitted", color: .purple),
            .askRerun: .init(icon: Image(systemName: "arrow.clockwise"), text: "Rerun Requested", color: .yellow),
            .serverCrash: .init(icon: Image(systemName: "exclamationmark.triangle"), text: "Server Error", color: .red),
            .executedSuccessfully: .init(icon: Image(systemName: "checkmark.circle"), text: "Executed Successfully", color: .green),
            .executionError: .init(icon: Image(systemName: "xmark.octagon"), text: "Execution Error", color: .red),
            .rawText: .init(icon: Image(systemName: "checkmark.circle"), text: "Response Received", color: .green)
        ]

        return appearance[self.statusCode] ?? .init(icon: Image(systemName: "questionmark"), text: "Unknown Status", color: .black)
    }
}
