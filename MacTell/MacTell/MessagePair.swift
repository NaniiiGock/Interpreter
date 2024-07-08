//
//  MessagePair.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import Foundation
import SwiftUI



class MessagePair: Identifiable, ObservableObject {
    let id: UUID
    let userInput: String
    @Published var llmResponse: String
    @Published var isSaved: Bool
    @Published var statusCode: StatusCode
    let date: String

    @Published var stdOut: String
    @Published var stdErr: String

    init(id: UUID = UUID(),
         userInput: String = "",
         llmResponse: String = "",
         isSaved: Bool = false,
         statusCode: StatusCode = .noActionTaken,
         date: String = getFormattedDate(date: Date()),
         stdOut: String = "",
         stdErr: String = "") {
    self.id = id
    self.userInput = userInput
    self.llmResponse = llmResponse
    self.isSaved = isSaved
    self.statusCode = statusCode
    self.date = date

    self.stdOut = stdOut
    self.stdErr = stdErr
}

    func buildJSONAndSendToServer(statusCode: StatusCode, modifyStatus: Bool) {
        var userServerInteractionData = UserServerInteractionDataBuilder().build_all(messagePair: self)
        userServerInteractionData.statusCode = statusCode

        WebSocketManager.shared.sendMessage(userServerInteractionData)

        if modifyStatus {
            self.statusCode = statusCode
        }
    }

    func sendInputTextToLLM() {
        self.buildJSONAndSendToServer(statusCode: .submitUserResponse, modifyStatus: true)
    }

    func toggleBookmark() {
        self.buildJSONAndSendToServer(statusCode: self.isSaved ? .removeFromBookmarks : .saveToBookmarks, modifyStatus: false)
        self.isSaved.toggle()
    }

    func addToBookmarks() {
        assert(!self.isSaved)
        self.toggleBookmark()
    }

    func rerunMe() {
        self.buildJSONAndSendToServer(statusCode: .askRerun, modifyStatus: true)
    }
    
    func confirmExecution() {
        self.buildJSONAndSendToServer(statusCode: .confirmExecution, modifyStatus: false)
        self.statusCode = .requestSentToAPI
    }

    func processReceivedData(userServerInteractionData: UserServerInteractionData) {
        self.statusCode = userServerInteractionData.statusCode

        switch userServerInteractionData.statusCode {
        case .sentForExecution, .askConfirmation, .rawText:
            self.llmResponse = userServerInteractionData.llmResponse
        case .requestSentToAPI, .serverCrash:
            return
        case .executedSuccessfully, .executionError:
            self.stdOut = userServerInteractionData.StdOut
            self.stdErr = userServerInteractionData.StdErr
        default:
            print("ERROR: MessagePair does not support such Status Code:", userServerInteractionData.statusCode)
        }
    }
}



struct MessageView: View {
    @ObservedObject var messagePair: MessagePair
    @State private var showOutputPopover = false
    var onDelete: ((MessagePair) -> Void)?
    
    @State private var isHovering = false

    var body: some View {
        
        ZStack(alignment: .topTrailing) {
            HStack(alignment: .firstTextBaseline, spacing: 10) {
                VStack(alignment: .leading, spacing: 5) {
                    
                    
                    
                    HStack(alignment: .top) {
                        Image(systemName: "person.fill")
                            .imageScale(.medium)
                            .foregroundColor(.blue)
                        Text(self.messagePair.userInput)
                    }
                
                    HStack(alignment: .top) {
                        Image(systemName: "cpu")
                            .imageScale(.small)
                            .foregroundColor(.purple)

                        Text(self.messagePair.llmResponse)
                    }

                    Spacer()
                    Text(self.messagePair.date)
                        .font(.system(size: 10))
                        .foregroundColor(.gray)
                }
                Spacer()

                VStack(alignment: .trailing, spacing: 5) {
                    HStack {
                        Button(action: { self.messagePair.toggleBookmark() }) {
                            Image(systemName: self.messagePair.isSaved ? "bookmark.fill" : "bookmark")
                        }

                        Button(action: { self.messagePair.statusCode == StatusCode.askConfirmation ? self.messagePair.confirmExecution() : self.messagePair.rerunMe() }) {
                            Image(systemName: self.messagePair.statusCode == StatusCode.askConfirmation ? "checkmark" : "play")
                        }
                    }

                    Spacer()

                    HStack {
                        if !self.messagePair.stdOut.isEmpty || !self.messagePair.stdErr.isEmpty {
                            Button(action: { self.showOutputPopover.toggle() }) {
                                Text(showOutputPopover ? "Hide Output" : "Show Output")
                                // Image(systemName: "chevron.down.circle.fill")
                            }
                            .popover(isPresented: $showOutputPopover) {
                                OutputPopoverView(stdOut: self.messagePair.stdOut, stdErr: self.messagePair.stdErr)
                            }
                        }
                        
                        
                        let statusAppearance = self.messagePair.getStatusAppearance()

                        statusAppearance.icon
                        Text(statusAppearance.text)
                            .foregroundColor(statusAppearance.color)
                    }


                }
            }
            .padding()
            .background(Color.gray.opacity(0.2))
            .cornerRadius(10)
            .padding()
            
            if onDelete != nil {
                Button(action: { self.onDelete?(self.messagePair) }) {
                    Image(systemName: "xmark")
                        .imageScale(.small) // Adjusts the scale of the image
                        .font(.system(size: 12)) // Adjusts the size of the image

                        .foregroundColor(.white) // Changing text color to white for contrast
                        .padding(3) // Adjust padding for touch area, slightly increased for better touch target
                }
                .onHover {hovering in
                            self.isHovering = hovering
                }
                .background(Color.black) // Changing background to black for a darker appearance
                .opacity(self.isHovering ? 0.7 : 0.3)
                .cornerRadius(20) // Keeping the circular shape
                .padding([.top, .trailing], 3) // Adjust padding to position the button correctly
                
            }
        }

    }
}

struct OutputPopoverView: View {
    var stdOut: String
    var stdErr: String

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            if !stdOut.isEmpty {
                Text("Standard Output:")
                    .fontWeight(.bold)
                Text(stdOut)
            }
            if !stdErr.isEmpty {
                Text("Standard Error:")
                    .fontWeight(.bold)
                Text(stdErr)
                    .foregroundColor(.orange).opacity(0.9)
            }
        }
        .padding()
    }
}


struct MessageView_Previews: PreviewProvider {
    struct PreviewWrapper: View {
        @State var sampleMessagePair = MessagePair(userInput: "Sample input", llmResponse: "Some LLM Response", statusCode: .executedSuccessfully, stdOut: "Nice",  stdErr: "WOWWWWW")

        var body: some View {
            MessageView(messagePair: self.sampleMessagePair)
        }
    }

    static var previews: some View {
        PreviewWrapper()
    }
}
